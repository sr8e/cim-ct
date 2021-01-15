import zlib

from pathlib import Path
from PIL import Image


class ConversionError(Exception):
    def __init__(self, message, path):
        self.message = message
        self.path = path


class IncorrectHeaderError(ConversionError):
    pass


class UnsupportedFormatError(ConversionError):
    pass


class DoesNotExistError(ConversionError):
    pass


class IncorrectPathError(ConversionError):
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

    def __init__(self, is_to_png, is_single, source, savepath=None):
        srcpath = Path(source)

        self.is_to_png = is_to_png
        self.is_single = is_single
        self.srcpath = srcpath
        self.savepath = savepath

        # validate
        if not srcpath.exists():
            raise DoesNotExistError('File or Directory Does Not Exist.', srcpath)

        if savepath is not None and not savepath.exists():
            raise DoesNotExistError(f'Save Directory Does Not Exist: {savepath}', srcpath)

        if is_single:
            if not srcpath.is_file():
                raise IncorrectPathError('Specified Path is not Correct.', srcpath)
        else:
            if not srcpath.is_dir():
                raise IncorrectPathError('Specified Path is not Correct.', srcpath)

    def execute(self):
        if self.is_to_png:
            if self.is_single:
                return self.cim_to_png(self.srcpath, self.savepath)
            else:
                return self.dir_to_png(self.srcpath, self.savepath)
        else:
            if self.is_single:
                return self.png_to_cim(self.srcpath, self.savepath)
            else:
                return self.dir_to_cim(self.srcpath, self.savepath)

    def dir_to_png(self, directory, savepath=None):
        for child in directory.iterdir():
            if child.suffix == '.cim':
                yield self.cim_to_png(child, savepath)

    def cim_to_png(self, file, savepath=None):

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

    def dir_to_cim(self, directory, savepath=None):
        for child in directory.iterdir():
            if child.suffix == '.png':
                self.png_to_cim(child, savepath)

    def png_to_cim(self, file, savepath=None):
        pass
