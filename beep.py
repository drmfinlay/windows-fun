#!/usr/bin/python
#
# BSD 2-Clause License
#
# Copyright (c) 2025, Dane Finlay
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
A utility for playing a specified beep sound through the sound card.
"""

import argparse
import sys

import win32api


def main():
    # Define program arguments.
    parser = argparse.ArgumentParser(
        prog="beep.py",
        description="This utility plays a beep sound through the sound card"
                    " with the specified frequency (in hertz) and duration"
                    " (in milliseconds). It is a thin wrapper around the"
                    " Win32 Beep() function and so behaves the same way."
    )
    parser.add_argument(
        "freq", type=int,
        help="The frequency of the sound, in hertz.  This parameter must be"
             " in the range 37 through 32,767 (0x25 through 0x7FFF)."
    )
    parser.add_argument(
        "duration", type=int,
        help="The duration of the sound, in milliseconds."
    )

    # Parse program arguments, exiting on error.
    args = parser.parse_args()

    # Beep as specified.
    res = win32api.Beep(args.freq, args.duration)

    # Use the success of the function as the exit code.
    return res


if __name__ == '__main__':
    exit(main())

