import re

from ftptool import FTPHost

from app.dwd_module.dwd_constant import *
from app.models import Response400


class FtpFileFinder:
    """
    connection to remote FTP server ( DWD ) will be established and a walk throw it possible.
    """
    paths = []
    file_path = ''
    ftp = None

    def __init__(self):
        """
        The connection will be automatically done by initialising the class
        """
        self.try_to_connect()

    def try_to_connect(self):
        try:
            self.ftp = FTPHost.connect(DWD_SERVER, user = DWD_USERNAME, password = DWD_PASSWORD, timeout = 20)


        except IOError as e:
            #raise ValueError(f'I/O error({e.errno}): {e.strerror}')
           return Response400(code=e.errno, message=e.strerror)
        # print(f'I/O error({e.errno}): {e.strerror}')
        # print("Retrying...")

    def findFile(self, start_path, find_pattern, ignore_pattern):
        """
        Query the FTP server and search for a file with the aid of pattern
        and ignore the unwanted files with the same pattern.
        :param start_path: string, where to search *start from root path {/}
        :param find_pattern: regular expression pattern
        :param ignore_pattern: regular expression pattern
        :return:list, where the first value stand for all paths found

        """

        for (dirname, subdirs, files) in self.ftp.walk(start_path):

            for file in files:

                file_finder = re.finditer(find_pattern, file, re.S)

                meta_pattern = re.compile(ignore_pattern)

                meta_match = meta_pattern.match(file)

                if not meta_match and file_finder:

                    for filename in file_finder:
                        self.file_path = dirname + "/" + filename.group( )

                        self.paths.append(self.file_path)

        return self.paths
