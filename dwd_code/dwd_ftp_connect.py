import re

from ftptool import FTPHost
from dwd_code.dwd_constant import *

def connect(server, username, password):
    """
    :param server:
    :param username:
    :param password:
    :return:
    """

    host = FTPHost.connect(server, user = username, password = password)

    return host

def FtpSearch(resolution, observation_type, stationId):
    """
    :param resolution:
    :param observation_type:
    :param stationId:
    :return: an Array (where all matched files found) & the File path
    """

    host = connect(DWD_SERVER, DWD_USERNAME, DWD_PASSWORD)
    #st_id = f"{stationId:05d}"

    choices_tuple = []

    if observation_type != None and resolution != None:

        walk_path = PATH_TO_WALK +  resolution + "/" + observation_type

    else:

        walk_path = PATH_TO_WALK

    for (dirname, subdirs, files) in host.walk(walk_path):

        for file in files:

            file_finder = re.finditer(r'.*' + str(stationId) + '.*', file, re.S)

            meta_pattern = re.compile(r'^Meta_Daten.*')

            meta_match = meta_pattern.match(file)

            if not meta_match and file_finder:

                for filename in file_finder:

                    file_path = dirname + "/" + filename.group( )

                    choices_tuple.append(file_path)

    return choices_tuple, file_path