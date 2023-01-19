#
# BSD 2-Clause License
#
# Copyright (c) 2023, Dane Finlay
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
EnablePointerPrecision

This program enables the 'Enhance pointer precision' setting available in
the Windows control panel under Mouse->Pointer Options.

I have included an option for delaying the change by N seconds:

    python.exe EnablePointerPecision.py /d 100

"""

import ctypes
import sys
import time


SPIF_SENDCHANGE = 0x0002
SPI_GETMOUSE    = 0x0003
SPI_SETMOUSE    = 0x0004


def main(args):
    # Delay, if necessary.
    delay = 0
    if len(args) == 2 and args[0].lower() == '/d':
        try: delay = float(args[1])
        except (ValueError, TypeError): return 1
    elif len(args) != 0:
        return 1

    if delay:
        time.sleep(delay)
        
    # Array: int[2]
    ThreeIntegers = ctypes.c_int * 3

    # Use SystemParametersInfoA to get the current values.
    SystemParametersInfoA = ctypes.windll.user32.SystemParametersInfoA
    mouseParams = ThreeIntegers(0, 0, 0)
    result = SystemParametersInfoA(SPI_GETMOUSE, 0, mouseParams, 0)
    if not result: return 2

    # Use SystemParametersInfoA to enable pointer precision, if necessary.
    # Leave the first two threshold values unchanged.
    if mouseParams[2] == 1: return 0
    mouseParams[2] = 1
    result = SystemParametersInfoA(SPI_SETMOUSE, 0, mouseParams, SPIF_SENDCHANGE)
    return 0 if result else 2


if __name__ == '__main__':
    returncode = main(sys.argv[1:])
    exit(returncode)
