import re
from typing import List

from app.dwd_module.dwd_file_finder import FtpFileFinder, PATH_TO_WALK


class Capabilities:
    """
    Query the DWD FTP service by a specified station
    """
    stationId: str = ''
    all_files: List[str] = []

    def __init__(self, stationId):
        """

        :param stationId: String *required
        """
        self.stationId = stationId
        self.all_files = FtpFileFinder().findFile(self.generateWalkPath(),
                                                  r'.*' + self.stationId + '.*', r'^Meta_Daten.*')

    def get_capabilities_by_station_id(self):

        """
        Search for the Capabilities for each given station Id
        :return: Dictionary
        """
        temporary1 = []
        temporary2 = []
        temporary3 = []
        temporary4 = []
        temporary5 = []

        for single_file in self.all_files:

            path_name = re.split('climate/', single_file)[-1]

            if path_name.startswith('10_minutes'):

                path_split = path_name.split('/')
                temporary1.append(path_split[1])

            elif path_name.startswith('1_minute'):

                path_split = path_name.split('/')
                temporary2.append(path_split[1])

            elif path_name.startswith('daily'):
                path_split = path_name.split('/')
                temporary3.append(path_split[1])

            elif path_name.startswith('hourly'):
                path_split = path_name.split('/')
                temporary4.append(path_split[1])

            elif path_name.startswith('monthly'):
                path_split = path_name.split('/')
                temporary5.append(path_split[1])

        list_format1 = list(dict.fromkeys(temporary1))  # To remove the duplication in the dict.
        list_format2 = list(dict.fromkeys(temporary2))
        list_format3 = list(dict.fromkeys(temporary3))
        list_format4 = list(dict.fromkeys(temporary4))
        list_format5 = list(dict.fromkeys(temporary5))

        dicto = dict(stationId = self.stationId, capabilities = [
            dict(resolution = "10_minutes", observationTypes = list_format1),
            dict(resolution = "1_minute", observationTypes = list_format2),
            dict(resolution = "daily", observationTypes = list_format3),
            dict(resolution = "hourly", observationTypes = list_format4),
            dict(resolution = "monthly", observationTypes = list_format5)
        ])

        return (dicto)

    def generateWalkPath(self):
        return PATH_TO_WALK
