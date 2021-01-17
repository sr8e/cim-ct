import zlib

from pathlib import Path
from PIL import Image


class BaseError(Exception):
    def __init__(self, message, path):
        self.message = message
        self.path = path

    def __str__(self):
        return f'{self.message} at {self.path}'


class ConversionError(BaseError):
    pass


class PathError(BaseError):
    pass


class IncorrectHeaderError(ConversionError):
    pass


class UnsupportedFormatError(ConversionError):
    pass


class DoesNotExistError(PathError):
    pass


class IncorrectPathError(PathError):
    pass


class CimConverter:
    formats = {
        3: "RGB",
        4: "RGBA",
    }

    pixel_size = {
        3: 3,
        4: 4,
    }

    def __init__(self, is_to_png, is_single, source, savepath=None, mkdir=False):
        srcpath = Path(source)
        dstpath = Path(savepath) if savepath is not None else None

        self.is_to_png = is_to_png
        self.is_single = is_single
        self.srcpath = srcpath
        self.dstpath = dstpath

        # validate
        if not srcpath.exists():
            raise DoesNotExistError('File or Directory Does Not Exist.', srcpath)

        if dstpath is not None:
            if dstpath.exists() and not dstpath.is_dir():
                raise IncorrectPathError(f'Specified Path Already Exists, and is not Directory: {dstpath}', srcpath)
            elif not dstpath.exists():
                if mkdir:
                    dstpath.mkdir(parents=True, exist_ok=True)
                else:
                    raise DoesNotExistError(f'Save Directory Does Not Exist: {dstpath}', srcpath)

        if is_single:
            if not srcpath.is_file():
                raise IncorrectPathError('Specified Path is not Correct.', srcpath)
        else:
            if not srcpath.is_dir():
                raise IncorrectPathError('Specified Path is not Correct.', srcpath)

    def execute(self):
        if self.is_to_png:
            if self.is_single:
                return self.cim_to_png(self.srcpath, self.dstpath)
            else:
                return self.dir_to_png(self.srcpath, self.dstpath)
        else:
            if self.is_single:
                return self.png_to_cim(self.srcpath, self.dstpath)
            else:
                return self.dir_to_cim(self.srcpath, self.dstpath)

    def dir_to_png(self, directory, dstpath=None):
        for child in directory.iterdir():
            if child.suffix == '.cim':
                yield self.cim_to_png(child, dstpath)

    def cim_to_png(self, file, dstpath=None):

        with file.open('rb') as f:
            bytes_arr = zlib.decompress(f.read())

        w = int.from_bytes(bytes_arr[:4], 'big')
        h = int.from_bytes(bytes_arr[4:8], 'big')
        fmt = int.from_bytes(bytes_arr[8:12], 'big')

        if w * h * self.pixel_size[fmt] != (body_size := len(bytes_arr) - 12):
            raise IncorrectHeaderError(f'Incorrect Header: w {w} * h {h} != body size {body_size}', file)

        if fmt not in self.formats:
            raise UnsupportedFormatError(f'Unsupported Format: {fmt}', file)

        im = Image.frombytes(self.formats[fmt], (w, h), bytes_arr[12:])

        dst = file.with_suffix('.png')
        if savepath is not None:
            dst = savepath / dst.name

        with dst.open("wb") as fw:
            im.save(fw, format="png")

        return f'Conversion Successfully Finished. {file}'

    def dir_to_cim(self, directory, dstpath=None):
        for child in directory.iterdir():
            if child.suffix == '.png':
                yield self.png_to_cim(child, dstpath)

    def png_to_cim(self, file, dstpath=None):
        pass
