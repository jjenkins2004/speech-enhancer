#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "rnnoise.h"
#include <numpy/arrayobject.h>
#include <Python.h>

#define FRAME_SIZE 480


// takes numpy array and does noise reduction process
static PyObject * rnnoise_process(PyObject *self, PyObject *args) {
    PyObject *input_obj;

    // Parse the input arguments: expect one object (should be a NumPy array).
    if (!PyArg_ParseTuple(args, "O", &input_obj)) {
        return NULL;
    }

    // Convert the input object to a NumPy array of type double (NPY_DOUBLE)
    PyArrayObject *array = (PyArrayObject *) PyArray_FROM_OTF(input_obj, NPY_FLOAT, NPY_ARRAY_IN_ARRAY | NPY_ARRAY_WRITEABLE);
    if (array == NULL) {
        return NULL;
    }

    // convert to float* array
    float *data = (float *)PyArray_DATA(array);

    // getting size
    npy_intp size = PyArray_SIZE(array);
    printf("Array size: %ld\n", size);
    printf("theres no way this actually works this is so cool");
    data[0] = 0;


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
    {NULL, NULL, 0, NULL}
};

// module definition structure
static struct PyModuleDef rnnoisemodule = {
    PyModuleDef_HEAD_INIT,
    "noise_reduction",
    "module that processes raw audio numpy data using rnnoise",  
    -1,         
    NumpyMethods
};

// Module initialization function (for Python 3)
PyMODINIT_FUNC PyInit_noise_reduction(void) {
    PyObject *module = PyModule_Create(&rnnoisemodule);
    if (module == NULL) {
        return NULL;
    }
    import_array();
    return module;
}