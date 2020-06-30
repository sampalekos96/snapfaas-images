#include <Python.h>
#include <stdlib.h>

static char *a = NULL;

static PyObject *
alloc_array(PyObject *self, PyObject *args) {
    int i;
    unsigned long n;
    if (!PyArg_ParseTuple(args, "k", &n)) {
        PyErr_SetString(PyExc_TypeError, "An integer parameter is required");
        Py_RETURN_NONE;
    }
    a = (char *)calloc((size_t) n, 1);
    if (a == NULL)
        PyErr_SetString(PyExc_MemoryError, "Out of memory");
    for (i = 0; i < n; ++i) {
        a[i] = 0;
    }
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

PyMODINIT_FUNC
initdummy_array(void) {
    (void) Py_InitModule("dummy_array", DummyMethods);
}
