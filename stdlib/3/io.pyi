# Stubs for io

from typing import (
    List, BinaryIO, TextIO, Iterator, Union, Optional, Callable, Tuple
)
import builtins
import codecs
import sys
from types import TracebackType

DEFAULT_BUFFER_SIZE = ...  # type: int

SEEK_SET = ...  # type: int
SEEK_CUR = ...  # type: int
SEEK_END = ...  # type: int

open = builtins.open

# FIXME when mypy handle condtional, we can uncomment the next block and remove
# the temporary fix
#if sys.version_info >= (3, 3):
#    BlockingIOError = BlockingIOError
#    class UnsupportedOperation(OSError, ValueError): ...
#else:
#    class BlockingIOError(IOError):
#        characters_written = ...  # type: int
#    class UnsupportedOperation(IOError, ValueError): ...
class BlockingIOError(OSError):
    characters_written = ...  # type: int
class UnsupportedOperation(OSError, ValueError): ...


class IOBase:
    def __iter__(self) -> Iterator[bytes]: ...
    def __next__(self) -> bytes: ...
    def __enter__(self) -> 'IOBase': ...
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception],
                 exc_tb: Optional[TracebackType]) -> bool: ...
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def readlines(self, hint: int = ...) -> List[bytes]: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def truncate(self, size: Optional[int] = ...) -> int: ...
    def writable(self) -> bool: ...
    def writelines(self, lines: bytes) -> None: ...
    if sys.version_info >= (3, 4):
        def readline(self, size: int = ...) -> bytes: ...
        def __del__(self) -> None: ...
    else:
        def readline(self, limit: int = ...) -> bytes: ...  # type: ignore
    if sys.version_info >= (3, 2):
        closed = ...  # type: bool
    else:
        def closed(self) -> bool: ...  # type: ignore

class RawIOBase(IOBase):
    def readall(self) -> bytes: ...
    def readinto(self, b: bytearray) -> Optional[int]: ...
    def write(self, b: Union[bytes, bytearray]) -> Optional[int]: ...
    if sys.version_info >= (3, 4):
        def read(self, size: int = ...) -> Optional[bytes]: ...
    else:
        def read(self, n: int = ...) -> Optional[bytes]: ...  # type: ignore

class BufferedIOBase(IOBase):
    def detach(self) -> 'RawIOBase': ...
    def readinto(self, b: bytearray) -> int: ...
    def write(self, b: Union[bytes, bytearray]) -> int: ...
    if sys.version_info >= (3, 5):
        def readinto1(self, b: bytearray) -> int: ...
    if sys.version_info >= (3, 4):
        def read(self, size: Optional[int] = ...) -> bytes: ...
        def read1(self, size: int = ...) -> bytes: ...
    else:
        def read(self, n: Optional[int] = ...) -> bytes: ...  # type: ignore
        def read1(self, n: int = ...) -> bytes: ...  # type: ignore


class FileIO(RawIOBase):
    mode = ...  # type: str
    name = ...  # type: Union[int, str]
    if sys.version_info >= (3, 3):
        def __init__(self, name: Union[str, bytes, int], mode: str = ...,
                     closefd: bool = ...,
                     opener: Optional[
                         Callable[[Union[int, str], str], int]] = ...) \
                     -> None: ...
    else:
        def __init__(self, name: Union[str, bytes, int],  # type: ignore
                     mode: str = ..., closefd: bool = ...) -> None: ...


class BytesIO(BufferedIOBase):
    def __init__(self, initial_bytes: bytes = ...) -> None: ...
    def getvalue(self) -> bytes: ...
    if sys.version_info >= (3, 2):
        def getbuffer(self) -> memoryview: ...

class BufferedReader(BufferedIOBase):
    def __init__(self, raw: RawIOBase, buffer_size: int = ...) -> None: ...
    if sys.version_info >= (3, 4):
        def peek(self, size: int = ...) -> bytes: ...
    else:
        def peek(self, n: int = ...) -> bytes: ...  # type: ignore

class BufferedWriter(BufferedIOBase):
    def __init__(self, raw: RawIOBase, buffer_size: int = ...) -> None: ...
    def flush(self) -> None: ...
    def write(self, b: Union[bytes, bytearray]) -> int: ...

class BufferedRandom(BufferedReader, BufferedWriter):
    def __init__(self, raw: RawIOBase, buffer_size: int = ...) -> None: ...
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def tell(self) -> int: ...

class BufferedRWPair(BufferedIOBase):
    def __init__(self, reader: RawIOBase, writer: RawIOBase,
                 buffer_size: int = ...) -> None: ...


class TextIOBase(IOBase):
    encoding = ...  # type: str
    errors = ...  # type: Optional[str]
    newlines = ...  # type: Union[str, Tuple[str, ...], None]
    def __iter__(self) -> Iterator[str]: ...  # type: ignore
    def __next__(self) -> str: ...  # type: ignore
    def __enter__(self) -> 'TextIOBase': ...
    def detach(self) -> IOBase: ...
    def write(self, s: str) -> int: ...
    if sys.version_info >= (3, 4):
        def readline(self, size: int = ...) -> str: ...  # type: ignore
        def read(self, size: Optional[int] = ...) -> str: ...
    elif sys.version_info >= (3, 2):
        def readline(self, limit: int = ...) -> str: ...  # type: ignore
    else:
        def readline(self) -> str: ...  # type: ignore
    if sys.version_info >= (3, 2):
        def seek(self, offset: int, whence: int = ...) -> int: ...
        def tell(self) -> int: ...

class TextIOWrapper(TextIOBase):
    line_buffering = ...  # type: bool
    if sys.version_info >= (3, 3):
        def __init__(self, buffer: BufferedIOBase, encoding: str = ...,
                     errors: Optional[str] = ..., newline: Optional[str] = ...,
                     line_buffering: bool = ..., write_through: bool = ...) \
                     -> None: ...
    else:
        def __init__(self, buffer: BufferedIOBase,  # type: ignore
                     encoding: str = ..., errors: Optional[str] = ...,
                     newline: Optional[str] = ..., line_buffering: bool = ...) \
                     -> None: ...

class StringIO(TextIOWrapper):
    def __init__(self, initial_value: str = ...,
                 newline: Optional[str] = ...) -> None: ...
    def getvalue(self) -> str: ...

class IncrementalNewlineDecoder(codecs.IncrementalDecoder): ...
