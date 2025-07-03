# windows-fun
Some Python code and programs using the Windows API.

Most of the *windows-fun* repo requires the pywin32 package to be installed.

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

## beep.py
A utility program for playing a specified beep sound through the sound card.
This is a thin wrapper around the Win32 Beep() function.

The following incantation will cause a beep of 550 Hz to be played through
the system sound card for 500 ms:

```
python.exe beep.py 550 500
```

As a side note, I wrote this utility for use with the built-in Windows
*timeout* utility, for beeping after thirty seconds:

```
timeout /nobreak /t 30 && beep 550 500
```

This works if *beep.py* is on your *PATH* and the *PATHEXT* list includes
\*.py.
