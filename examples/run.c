/*
compilation command:
x86_64-w64-mingw32-gcc -Wall -Os -municode -mwindows -Iinclude -Llibs -s -o run314.exe run.c -lpython314
*/

#include <windows.h>
#include <Python.h>

#define BUFFER_SIZE 4096
wchar_t buffer[BUFFER_SIZE];

int ErrorCode(PyObject *exception, const char *name)
{
  PyObject *code;
  code = PyObject_GetAttrString(exception, name);
  if(code != NULL && PyLong_Check(code)) return PyLong_AsLong(code);
  else return -1;
}

int HandleException()
{
  PyObject *exception, *message;
  exception = PyErr_GetRaisedException();
  if(PyObject_IsInstance(exception, PyExc_SystemExit)) return ErrorCode(exception, "code");
  message = PyObject_Str(exception);
  PyUnicode_AsWideChar(message, buffer, BUFFER_SIZE);
  MessageBoxW(NULL, buffer, NULL, MB_ICONERROR);
  return ErrorCode(exception, "errno");
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow)
{
  wchar_t *name, *dot;
  PyObject *module, *runpy, *method, *main, *result;
  PyConfig config;

  SetProcessDPIAware();

  GetModuleFileNameW(NULL, buffer, BUFFER_SIZE);

  PyConfig_InitIsolatedConfig(&config);
  PyConfig_SetArgv(&config, __argc, __wargv);
  PyConfig_SetString(&config, &config.program_name, buffer);
  Py_InitializeFromConfig(&config);
  PyConfig_Clear(&config);

  name = wcsrchr(buffer, L'\\');
  if(name != NULL) ++name;
  else name = buffer;

  dot = wcsrchr(name, L'.');
  if(dot != NULL) *dot = L'\0';

  module = PyUnicode_FromWideChar(name, wcslen(name));
  method = PyUnicode_FromString("run_module");
  main = PyUnicode_FromString("__main__");
  runpy = PyImport_ImportModule("runpy");
  result = PyObject_CallMethodObjArgs(runpy, method, module, Py_None, main, NULL);

  if(result != NULL) return 0;
  else return HandleException();
}
