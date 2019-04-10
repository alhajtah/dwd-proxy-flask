import re
from ftplib import FTP

from ftptool import FTPHost
from pystache import render

from dwd_code.dwd_constant import *


class FtpFileFinder:
    """
    connection to remote FTP server ( DWD ) will be established and a walk throw it possible.
    """
    paths = []
    file_path = ''
    ftp = None

    def __init__(self):
        """
        Test: The connection will be automatically repeated till responding
        """
        try:
            self.ftp = FTPHost.connect(DWD_SERVER, user = DWD_USERNAME, password = DWD_PASSWORD, timeout = 20)


        except IOError as e:
            raise  ValueError(f'I/O error({e.errno}): {e.strerror}')
             #print(f'I/O error({e.errno}): {e.strerror}')
            # print("Retrying...")

        # self.ftp = FTPHost.connect(DWD_SERVER, user = DWD_USERNAME, password = DWD_PASSWORD)

    def findFile(self, start_path, find_pattern, ignore_pattern):
        """

        :param start_path:
        :param find_pattern:
        :param ignore_pattern:
        :return:
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

        return self.paths, self.file_path


