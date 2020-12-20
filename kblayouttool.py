"""
kblayouttool

This is a utility program for working with Windows keyboard layouts. It can function
as a sort of command-line replacement for the Windows language bar.

"""

# pylint: disable=E0401
# This file imports Win32-only modules.

import argparse
import logging
import time

import win32api
import win32con
import win32gui
import win32process


#------------------------------------------------------------------------------------
# Win32 library functions.

def post_lang_change_request_message(hwnd, wparam, lparam):
    """ Post a WM_INPUTLANGCHANGEREQUEST message with the specified parameters. """
    win32gui.PostMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, wparam, lparam)


def get_current_layout():
    """
    Get the foreground window's current keyboard layout.

    :rtype: int
    :returns: current keyboard layout (HKL DWORD)
    """
    thread_id = win32process.GetWindowThreadProcessId(
        win32gui.GetForegroundWindow()
    )[0]

    # Return the HKL as a 32-bit unsigned integer.
    return win32api.GetKeyboardLayout(thread_id) & 0xffffffff


def get_all_layouts():
    """
    Get a list of all loaded keyboard layouts.

    :rtype: list
    :returns: keyboard layouts
    """
    # Return each HKL as a 32-bit unsigned integer.
    return [hkl & 0xffffffff for hkl in win32api.GetKeyboardLayoutList()]


def set_layout(wparam, lparam, broadcast):
    """
    Set the current keyboard layout by posting a WM_INPUTLANGCHANGEREQUEST message.

    :param wparam: WM_INPUTLANGCHANGEREQUEST message WPARAM value
    :type wparam: int
    :param lparam: WM_INPUTLANGCHANGEREQUEST message LPARAM value
    :type lparam: int
    :param broadcast: whether to post the request message to all windows
    :type broadcast: bool
    """
    # Post the request message to all windows, i.e. broadcast, if specified.
    # Otherwise, only post the request message to the foreground window.
    if broadcast:
        hwnd = win32con.HWND_BROADCAST
    else:
        hwnd = win32gui.GetForegroundWindow()

    # Post the request message.
    post_lang_change_request_message(hwnd, wparam, lparam)


#------------------------------------------------------------------------------------
# CLI functions.

def _cli_get_layout(args):
    # Delay getting the keyboard layout if a non-zero delay value was specified.
    delay = args.delay
    if delay:
        time.sleep(delay)

    # Get the current HKL and print it to stdout in hexadecimal format.
    hkl = get_current_layout()
    print("0x%08x" % hkl)

    # Return the success of this command.
    return 0


def _set_layout(args, wparam, lparam):
    # Delay setting the keyboard layout if a non-zero delay value was specified.
    delay = args.delay
    if delay:
        time.sleep(delay)

    # Set the keyboard layout as specified.
    set_layout(wparam, lparam, args.all_windows)

    # Return the success of this command.
    return 0


def _cli_set_layout(args):
    return _set_layout(args, 0, args.hkl)


def _cli_prev_layout(args):
    inputlangchange_backward = 0x0004
    return _set_layout(args, inputlangchange_backward, 0)


def _cli_next_layout(args):
    inputlangchange_forward = 0x0002
    return _set_layout(args, inputlangchange_forward, 0)


def _cli_list_layouts(args):
    # pylint: disable=W0613
    # Get and print each HKL to stdout in hexadecimal format.
    for hkl in get_all_layouts():
        print("0x%08x" % hkl)
    return 0


#------------------------------------------------------------------------------------
# argparse functions.

def _hexadecimal_or_int(string):
    try:
        return int(string)
    except ValueError:
        return int(string, 16)


def _build_argument(*args, **kwargs):
    return args, kwargs


def _add_arguments(parser, *arguments):
    for (args, kwargs) in arguments:
        parser.add_argument(*args, **kwargs)


def _get_cli_arguments():
    # Use argparse to parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Utility command-line program for working with Windows keyboard "
                    "layouts."
    )
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Build commonly used arguments.
    delay_argument = _build_argument(
        "-d", "--delay", default=0, type=float,
        help="Time in seconds to delay before getting/setting the keyboard "
        "layout."
    )
    all_windows_argument = _build_argument(
        "-a", "--all-windows", default=False, action="store_true",
        help="Change the keyboard layout for all windows instead of only the "
        "current foreground window. This may be useful on OS versions below "
        "Windows 8."
    )

    # Create the parser for the "get-layout" command.
    parser_get_layout = subparsers.add_parser(
        "get-layout",
        help="Print the current keyboard layout (HKL) of the foreground "
        "window. This value is used as an argument for other commands."
    )
    _add_arguments(parser_get_layout, delay_argument)

    # Create the parser for the "set-layout" command.
    parser_set_layout = subparsers.add_parser(
        "set-layout",
        help="Set the current keyboard layout."
    )
    hkl_argument = _build_argument(
        "hkl", type=_hexadecimal_or_int,
        help="An input locale identifier (HKL) corresponding to the keyboard layout "
        "to set."
    )
    _add_arguments(parser_set_layout, hkl_argument, all_windows_argument,
                   delay_argument)

    # Create the parser for the "prev-layout" command.
    parser_prev_layout = subparsers.add_parser(
        "prev-layout",
        help="Cycle backward one keyboard layout."
    )
    _add_arguments(parser_prev_layout, all_windows_argument,
                   delay_argument)

    # Create the parser for the "next-layout" command.
    parser_next_layout = subparsers.add_parser(
        "next-layout",
        help="Cycle forward one keyboard layout."
    )
    _add_arguments(parser_next_layout, all_windows_argument,
                   delay_argument)

    # Create the parser for the "list-layouts" command.
    subparsers.add_parser(
        "list-layouts",
        help="List each input locale identifier (HKL) corresponding to the current "
        "set of input locales in the system. These identifiers can be used with the "
        "'set-layout' command."
    )

    # Parse and return the arguments.
    return parser.parse_args()


#------------------------------------------------------------------------------------
# Main function.

def _main():
    # Set up logging.
    logging.basicConfig(format="%(levelname)s: %(message)s")
    log = logging.getLogger()

    # Parse arguments.
    args = _get_cli_arguments()

    def not_implemented(_):
        log.error("Command '%s' is not implemented.", args.command)
        return 1

    # Call the relevant CLI function and exit using the result.
    command_map = {
        "get-layout": _cli_get_layout,
        "set-layout": _cli_set_layout,
        "prev-layout": _cli_prev_layout,
        "next-layout": _cli_next_layout,
        "list-layouts": _cli_list_layouts,
    }
    func = command_map.get(args.command, not_implemented)
    return_code = func(args)
    exit(return_code)


if __name__ == '__main__':
    _main()
