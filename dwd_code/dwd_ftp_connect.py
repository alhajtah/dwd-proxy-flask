import re
from ftplib import FTP

from ftptool import FTPHost
from dwd_code.dwd_constant import *

class FtpFileFinder:

    """
    :param server:
    :param username:
    :param password:
    :return:
    """


    paths = []
    file_path = ''
    ftp = None
    resolution = ''
    observation_type = ''
    stationId = ''



    def __init__(self):

        retry = True
        while (retry):
            try:
                conn = FTP(DWD_SERVER)
                conn.connect( )
                self.ftp = FTPHost.connect(DWD_SERVER, user = DWD_USERNAME, password = DWD_PASSWORD)

                retry = False

            except IOError as e:
                # print(f'I/O error({e.errno}): {e.strerror}')
                # print("Retrying...")
                retry = True

        #self.ftp = FTPHost.connect(DWD_SERVER, user = DWD_USERNAME, password = DWD_PASSWORD)


    def FtpSearch(self, observation_type, stationId, resolution):
        """
        :param resolution:
        :param observation_type:
        :param stationId:
        :return: an Array (where all matched files found) & the File path
        """
        self.observation_type = observation_type
        self.resolution = resolution
        self.stationId = stationId

        if self.observation_type != '' and self.resolution != '':

            walk_path = PATH_TO_WALK +  self.resolution + "/" + self.observation_type

        else:

            walk_path = PATH_TO_WALK

        for (dirname, subdirs, files) in self.ftp.walk(walk_path):

            for file in files:

                file_finder = re.finditer(r'.*' + self.stationId + '.*', file, re.S)

                meta_pattern = re.compile(r'^Meta_Daten.*')

                meta_match = meta_pattern.match(file)

                if not meta_match and file_finder:

                    for filename in file_finder:

                        self.file_path = dirname + "/" + filename.group( )

                        self.paths.append(self.file_path)

        return self.paths, self.file_path