#include <Python.h>
#include <stdlib.h>

static void *a = NULL;

static PyObject *
alloc_array(PyObject *self, PyObject *args) {
    unsigned long n;
    if (!PyArg_ParseTuple(args, "k", &n)) {
        PyErr_SetString(PyExc_TypeError, "An integer parameter is required");
        Py_RETURN_NONE;
    }
    a = calloc((size_t) n, 1);
    if (a == NULL)
        PyErr_SetString(PyExc_MemoryError, "Out of memory");
    Py_RETURN_NONE;
}

static PyObject *
free_array() {
    free(a);
    //PyMem_Free((void *)a);
    Py_RETURN_NONE;
}

static PyMethodDef DummyMethods[] =
{
    {"alloc_array", (PyCFunction)alloc_array, METH_VARARGS, "allocate an array of n bytes"},
    {"free_array", (PyCFunction)free_array, METH_NOARGS, "free the array created by dummy_alloc_array"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef dummymodule = {
    PyModuleDef_HEAD_INIT,
    "dummy_array",  /* name of module */
    NULL,           /* module documentation, may be NULL */
    -1,             /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
    DummyMethods
};

PyMODINIT_FUNC
PyInit_dummy_array(void) {
    return PyModule_Create(&dummymodule);
}
