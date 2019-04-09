import datetime
import io
import re
import urllib
from zipfile import ZipFile
from dwd_code.dwd_constant import *


import pandas as pd

from dwd_code.dwd_ftp_connect import FtpFileFinder
from swagger_server import util
from swagger_server.models import Response, ResponseTimeseries, Values

class TimeSeries:


    stationId =''
    resolution = ''
    observation_type = ''
    start = None
    end = None
    path_choises = ''
    file_path = ''
    f_read = {}
    path = ''
    r_dict = {}
    all_rsp = {}

    def __init__(self, stationId,  resolution, observation_type, start, end):
        """

        :param stationId:
        :param resolution:
        :param observation_type:
        :param start:
        :param end:
        """

        self.stationId  = stationId
        self.resolution = resolution
        self.observation_type = observation_type
        self.start = start
        self.end = end
        self.path_choises, self.file_path = FtpFileFinder( ).FtpSearch(stationId = self.stationId,
                                                                       resolution = self.resolution,
                                                                       observation_type = self.observation_type)



    #def zip_extract(self,half_path):
    def zip_extract(self, path):
        """

        :param path:
        :return:
        """

        self.path = "ftp://" +DWD_SERVER +"/"+ path


        mysock = urllib.request.urlopen(self.path)

        memfile = io.BytesIO(mysock.read( ))

        with ZipFile(memfile, 'r') as myzip:
            nameList = myzip.namelist( )
            p = re.compile(r'^produkt.*')
            for name in nameList:
                m = p.match(name)
                if m:
                    filename = m.group( )
            f= myzip.open(filename)
            f_read = pd.read_csv(f, sep = ";")
            self.r_dict =f_read.to_dict('records')

        return self.r_dict



    def dwd_response(self):

        """

        :return:
        """





        resp = Response()  # type: Response
        resp.observation_type = self.observation_type
        resp.resolution =self.resolution
        resp.station_id= self.stationId
        resp.timeseries = []


        for singel_path in self.path_choises:

            self.r_dict = self.zip_extract(singel_path)
            path_split = singel_path.split('/')
            file_name = path_split[-1]
            epoch = path_split[-2]


            for i, d in enumerate(self.r_dict, 2):

                del d['STATIONS_ID']
                del d['eor']
                ts = ResponseTimeseries( )
                ts.epoch = epoch
                ts.source_line =  i
                ts.source_file = file_name
                ts.source_url = self.path
                ts.values = []





                for k, v in d.items( ):

                    if k != 'MESS_DATUM':
                        ts.values.append(Values(name = k, value = v))
                    else :
                        ts.timestamp = util.deserialize_datetime(str(v))



                resp.timeseries.append(ts)

            #break


        return resp
