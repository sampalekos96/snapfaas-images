`dummy-carray` is a module that implements two function calls:
1. alloc_array(n): calling `calloc` to allocate n bytes memory. The pointer is stored in a module
global variable.
2. free_array(): free the array allocated by the corresponding `alloc_array(n)`.

`noop-carray-[0-10]m` are noop Python3 serverless functions where the number indicates how many
mega bytes are allocated. The allocation happens at the time of function loading instead of when
a request arrives.
