import datetime
import io
import re
import urllib
from zipfile import ZipFile
from dwd_code.dwd_constant import *


import pandas as pd

from dwd_code.dwd_ftp_connect import FtpSearch
from swagger_server import util
from swagger_server.models import Response, ResponseTimeseries, Values

def dwd_responce(stationId, resolution, observation_type, file_path, r_dict):
    path = DWD_SERVER + '/' + file_path
    path_split = file_path.split('/')
    file_name = path_split[-1]
    epoch = path_split[-2]
    line_num = 0
    resp = Response(station_id = stationId, resolution = resolution,
                    observation_type = observation_type)  # type: Response
    ts = ResponseTimeseries(
        timestamp = datetime.datetime.now( ),
        epoch = epoch,
        source_file = file_name,
        source_url = path,
        source_line = line_num
    )
    ts.values = []
    for i, d in enumerate(r_dict, 2):
        del d['STATIONS_ID']
        del d['eor']

        for k, v in d.items( ):
            ts.values.append(Values(name = k, value = v))
    resp.timeseries = [ts]

    return resp

def zip_extract(half_path, stationId, resolution, observation_type):
    """

    :param half_path:
    :param stationId:
    :param resolution:
    :param observation_type:
    :return:
    """
    path = DWD_SERVER + half_path


    mysock = urllib.request.urlopen(path)

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
        r_dict =f_read.to_dict('records')









        #f_read['MESS_DATUM'] = util.deserialize_datetime( f_read['MESS_DATUM'].format(datetime.MINYEAR))
    return resp

def refomrTimeseries(path_choises):

    for half_path in path_choises:

        f_read = zip_extract(half_path)

    return f_read


def default(stationId, resolution, observation_type, start, end):
    """

    :param stationId:
    :param resolution:
    :param observation_type:
    :param start:
    :param end:
    :return:
    """
    # resp = (stationId, resolution, observation_type, start, end)
    res = FtpSearch(stationId = stationId, resolution = resolution, observation_type = observation_type)

    #responce = zip_ex(res[0], stationId, resolution, observation_type)



    # resp.timeseries = [ts]
    return res
