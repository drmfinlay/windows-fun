# windows-fun
Some Python code using the Windows API

## window change listener.py
A script using the Windows API to register for window focus changes and
print the titles of newly focused windows.

## kblayouttool.py
A utility program for working with Windows keyboard layouts. It can function
as a sort of command-line replacement for the Windows language bar.

The module also has a few useful keyboard-related library functions.

## EnablePointerPrecision.py

A simple program for enabling the *Enhanced pointer precision* setting
available in the Windows control panel  under Mouse->Pointer Options.

I have included a Windows-style option (/d) for delaying the change by *N*
seconds.

```
python.exe EnablePointerPecision.py /d 100
```
