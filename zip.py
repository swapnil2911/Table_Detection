import zipfile
# Utilize mmap module to avoid a potential DoS exploit (e.g. by reading the
# whole zip file into memory). A bad zip file example can be found here:
# https://bugs.python.org/issue24621

import mmap
from io import UnsupportedOperation
from zipfile import BadZipfile

zipfile_path = '/content/images.zip'

# The end of central directory signature
CENTRAL_DIRECTORY_SIGNATURE = b'\x50\x4b\x05\x06'


def repair_central_directory(zipFile):
    if hasattr(zipFile, 'read'):
        # This is a file-like object
        f = zipFile
        try:
            fileno = f.fileno()
        except UnsupportedOperation:
            # This is an io.BytesIO instance which lacks a backing file.
            fileno = None
    else:
        # Otherwise, open the file with binary mode
        f = open(zipFile, 'rb+')
        fileno = f.fileno()
    if fileno is None:
        # Without a fileno, we can only read and search the whole string
        # for the end of central directory signature.
        f.seek(0)
        pos = f.read().find(CENTRAL_DIRECTORY_SIGNATURE)
    else:
        # Instead of reading the entire file into memory, memory-mapped the
        # file, then search it for the end of central directory signature.
        # Reference: https://stackoverflow.com/a/21844624/2293304
        mm = mmap.mmap(fileno, 0)
        pos = mm.find(CENTRAL_DIRECTORY_SIGNATURE)
        mm.close()
    if pos > -1:
        # size of 'ZIP end of central directory record'
        f.truncate(pos + 22)
        f.seek(0)
        return f
    else:
        # Raise an error to make it fail fast
        print("error69")
        raise BadZipfile('File is not a zip file')

with zipfile.ZipFile(repair_central_directory(zipfile_path),"r") as zip_ref:

    zip_ref.extractall("/content/Table_Detection/images")