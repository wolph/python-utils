import contextlib
import os
import typing

from . import converters

Dimensions = typing.Tuple[int, int]
OptionalDimensions = typing.Optional[Dimensions]


def get_terminal_size() -> Dimensions:  # pragma: no cover
    '''Get the current size of your terminal

    Multiple returns are not always a good idea, but in this case it greatly
    simplifies the code so I believe it's justified. It's not the prettiest
    function but that's never really possible with cross-platform code.

    Returns:
        width, height: Two integers containing width and height
    '''
    w: typing.Optional[int]
    h: typing.Optional[int]

    with contextlib.suppress(Exception):
        # Default to 79 characters for IPython notebooks
        from IPython import get_ipython  # type: ignore

        ipython = get_ipython()
        from ipykernel import zmqshell  # type: ignore

        if isinstance(ipython, zmqshell.ZMQInteractiveShell):
            return 79, 24
    with contextlib.suppress(Exception):
        # This works for Python 3, but not Pypy3. Probably the best method if
        # it's supported so let's always try
        import shutil

        w, h = shutil.get_terminal_size()
        if w and h:
            # The off by one is needed due to progressbars in some cases, for
            # safety we'll always substract it.
            return w - 1, h
    with contextlib.suppress(Exception):
        w = converters.to_int(os.environ.get('COLUMNS'))
        h = converters.to_int(os.environ.get('LINES'))
        if w and h:
            return w, h
    with contextlib.suppress(Exception):
        import blessings  # type: ignore

        terminal = blessings.Terminal()
        w = terminal.width
        h = terminal.height
        if w and h:
            return w, h
    with contextlib.suppress(Exception):
        # The method can return None so we don't unpack it
        wh = _get_terminal_size_linux()
        if wh is not None and all(wh):
            return wh

    with contextlib.suppress(Exception):
        # Windows detection doesn't always work, let's try anyhow
        wh = _get_terminal_size_windows()
        if wh is not None and all(wh):
            return wh

    with contextlib.suppress(Exception):
        # needed for window's python in cygwin's xterm!
        wh = _get_terminal_size_tput()
        if wh is not None and all(wh):
            return wh

    return 79, 24


def _get_terminal_size_windows() -> OptionalDimensions:  # pragma: no cover
    res = None
    try:
        from ctypes import windll, create_string_buffer  # type: ignore

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except Exception:
        return None

    if res:
        import struct

        (_, _, _, _, _, left, top, right, bottom, _, _) = struct.unpack(
            "hhhhHhhhhhh", csbi.raw
        )
        w = right - left
        h = bottom - top
        return w, h
    else:
        return None


def _get_terminal_size_tput() -> OptionalDimensions:  # pragma: no cover
    # get terminal width src: http://stackoverflow.com/questions/263890/
    try:
        import subprocess

        proc = subprocess.Popen(
            ['tput', 'cols'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = proc.communicate(input=None)
        w = int(output[0])
        proc = subprocess.Popen(
            ['tput', 'lines'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = proc.communicate(input=None)
        h = int(output[0])
        return w, h
    except Exception:
        return None


def _get_terminal_size_linux() -> OptionalDimensions:  # pragma: no cover
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct

            return struct.unpack(
                'hh',
                fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'),  # type: ignore
            )
        except Exception:
            return None

    size = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not size:
        with contextlib.suppress(Exception):
            fd = os.open(os.ctermid(), os.O_RDONLY)  # type: ignore
            size = ioctl_GWINSZ(fd)
            os.close(fd)
    if not size:
        try:
            size = os.environ['LINES'], os.environ['COLUMNS']
        except Exception:
            return None

    return int(size[1]), int(size[0])
