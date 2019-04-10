import io
import re
import urllib
from zipfile import ZipFile

import pandas as pd

from dwd_code.dwd_constant import *
from dwd_code.dwd_file_finder import FtpFileFinder
from swagger_server import util
from swagger_server.models import Response, ResponseTimeseries, Values


class TimeSeries:
    """
    Query the DWD FTP service by a specified station, resolution and datatype and a optional timerange to filter
    the results.
    """
    stationId = ''
    resolution = ''
    observation_type = ''
    start = None
    end = None
    path_choices = ''
    file_path = ''
    f_read = {}
    path = ''
    r_dict = {}
    all_rsp = {}

    def __init__(self, stationId, resolution, observation_type, start, end):
        """
        Call the class ( FtpFileFinder ) and it's Method FtpSearch at first, so that the
        connection and the paths are ready to be used.
        :param stationId: string *required
        :param resolution: string *required
        :param observation_type: string *required
        :param start: Date time *not required
        :param end: Date time *not required
        """

        self.stationId = stationId
        self.resolution = resolution
        self.observation_type = observation_type
        self.start = start
        self.end = end
        self.path_choices, self.file_path = FtpFileFinder().findFile(
            self.generateWalkPathByResolutionAndStationId(),r'.*' + self.stationId + '.*', r'^Meta_Daten.*')




    def generateWalkPathByResolutionAndStationId(self):
        """

        :return:
        """
        return PATH_TO_WALK + self.resolution + "/" + self.observation_type


    def zip_extract(self, path):
        """
        unpacking a single zip file for a path.
        returns a dictionary sorted by records
        :param path: string
        :return: Dictionary
        """

        self.path = "ftp://" + DWD_SERVER + "/" + path

        mysock = urllib.request.urlopen(self.path)

        memfile = io.BytesIO(mysock.read( ))

        with ZipFile(memfile, 'r') as myzip:
            nameList = myzip.namelist( )
            p = re.compile(r'^produkt.*')
            for name in nameList:
                m = p.match(name)
                if m:
                    filename = m.group( )
            f = myzip.open(filename)
            f_read = pd.read_csv(f, sep = ";")
            self.r_dict = f_read.to_dict('records')

        return self.r_dict

    def dwd_response(self):

        """
        reforming the response to match with swagger definition
        :return: Dictionary
        """

        resp = Response( )  # type: Response
        resp.observation_type = self.observation_type
        resp.resolution = self.resolution
        resp.station_id = self.stationId
        resp.timeseries = []
        # timeseries = []

        for singel_path in self.path_choices:

            self.r_dict = self.zip_extract(singel_path)
            path_split = singel_path.split('/')
            file_name = path_split[-1]
            epoch = path_split[-2]

            for i, ditr in enumerate(self.r_dict, 2):

                del ditr['STATIONS_ID']
                del ditr['eor']

                ts = ResponseTimeseries( )
                ts.epoch = epoch
                ts.source_line = i
                ts.source_file = file_name
                ts.source_url = self.path
                ts.values = []

                for k, v in ditr.items( ):

                    if k != 'MESS_DATUM':
                        ts.values.append(Values(name = k, value = v))
                    else:
                        ts.timestamp = util.deserialize_datetime(str(v))

                resp.timeseries.append(ts)


                #break


        return resp
