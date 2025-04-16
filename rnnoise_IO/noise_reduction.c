#define NPY_NO_DEPRECATED_API NPY_2_0_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>
#include "rnnoise.h"
#include <stdbool.h>
#include <stdio.h>

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
    PyArrayObject *array = (PyArrayObject *)PyArray_FROM_OTF(input_obj, NPY_SHORT, NPY_ARRAY_INOUT_ARRAY);
    if (array == NULL)
    {
        return NULL;
    }

    // Checking if it is a 2D array
    if (PyArray_NDIM(array) != 2)
    {
        PyErr_SetString(PyExc_ValueError,
                        "expected a 2D array (channels × frames)");
        Py_DECREF(array);
        return NULL;
    }

    // Grabbing the array dimensions
    npy_intp *dims = PyArray_DIMS(array);
    npy_intp channels = dims[0];
    npy_intp frames = dims[1];

    // convert to short* array
    short *data = (short *)PyArray_DATA(array);

    printf("beginning rnnoise processing...\n");

    // loading in model
    RNNModel *model = NULL;
#ifdef USE_WEIGHTS_FILE
    model = rnnoise_model_from_filename("weights_blob.bin");
#endif

    for (npy_intp c = 0; c < channels; c++)
    {
        // defining variables
        DenoiseState *st;
        float tmp[FRAME_SIZE];
        npy_intp i;
        npy_intp j;
        bool first = true;

        // create a new model for each channel
        st = rnnoise_create(model);

        for (i = 0; i <= frames - 480; i += 480)
        {
            for (j = 0; j < FRAME_SIZE; j++)
            {
                tmp[j] = data[c * frames + i + j];
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
                data[c * frames + i + j] = tmp[j];
            }
        }
        rnnoise_destroy(st);
    }
    if (model)
    {
        rnnoise_model_free(model);
    }

    printf("finished rnnoise processing!\n");

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
    if (_import_array() < 0)
    {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}