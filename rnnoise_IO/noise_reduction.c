#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "rnnoise.h"
#include <numpy/arrayobject.h>
#include <Python.h>
#include <stdbool.h>

#define FRAME_SIZE 480

// takes numpy array and does noise reduction process
static PyObject *rnnoise_process(PyObject *self, PyObject *args)
{
    PyObject *input_obj;

    // parse the input arguments: expect one object (should be a NumPy array).
    if (!PyArg_ParseTuple(args, "O", &input_obj))
    {
        return NULL;
    }

    // convert the input object to a NumPy array of type short
    PyArrayObject *array = (PyArrayObject *)PyArray_FROM_OTF(input_obj, NPY_SHORT, NPY_ARRAY_IN_ARRAY | NPY_ARRAY_WRITEABLE);
    if (array == NULL)
    {
        return NULL;
    }
    size_t size = (size_t)PyArray_SIZE(array);

    // convert to short* array
    short *data = (short *)PyArray_DATA(array);

    // defining variables
    DenoiseState *st;
    float tmp[FRAME_SIZE];
    int i;
    int j;
    bool first = true;

    // loading in model
#ifdef USE_WEIGHTS_FILE
    RNNModel *model = rnnoise_model_from_filename("weights_blob.bin");
    st = rnnoise_create(model);
#else
    st = rnnoise_create(NULL);
#endif
    prinf("beginning rnnoise processing...")
    for (i = 0; i < size - 480; i += 480)
    {
        for (j = 0; j < FRAME_SIZE; j++)
        {
            tmp[j] = data[i + j];
        }
        rnnoise_process_frame(st, tmp, tmp);
        // dont write the first frame, model needs one initial frame
        if (first)
        {
            first = false;
            continue;
        }
        for (j = 0; j < FRAME_SIZE; j++)
        {
            data[i + j] = tmp[j];
        }
    }
    printf("finished rnnoise processing!")
    rnnoise_destroy(st);
#ifdef USE_WEIGHTS_FILE
    rnnoise_model_free(model);
#endif

    // Clean up
    Py_DECREF(array);
    Py_RETURN_NONE;
}

// module definitions
static PyMethodDef NumpyMethods[] = {
    {"rnnoise_process", rnnoise_process, METH_VARARGS,
     "Process raw audio data using RNNoise.\n\n"
     "Args:\n"
     "    data (numpy.ndarray): Input raw audio data as a NumPy array.\n"
     "Returns:\n"
     "    numpy.ndarray: Processed audio data."},
    {NULL, NULL, 0, NULL}};

// module definition structure
static struct PyModuleDef rnnoisemodule = {
    PyModuleDef_HEAD_INIT,
    "noise_reduction",
    "module that processes raw audio numpy data using rnnoise",
    -1,
    NumpyMethods};

// Module initialization function (for Python 3)
PyMODINIT_FUNC PyInit_noise_reduction(void)
{
    PyObject *module = PyModule_Create(&rnnoisemodule);
    if (module == NULL)
    {
        return NULL;
    }
    import_array();
    return module;
}