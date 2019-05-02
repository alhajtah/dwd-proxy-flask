import decimal
import io
import re
import urllib
import datetime
from zipfile import ZipFile

import pandas as pd
import pytz

from app.dwd_module.dwd_constant import *
from app.dwd_module.dwd_file_finder import FtpFileFinder
from app import util
from app.models import Response, ResponseTimeseries, Values


class TimeSeries:
    """
    Query the DWD FTP service by a specified station, resolution and datatype and a optional timerange to filter
    the results.
    """
    stationId = ''
    resolution = ''
    observation_type = ''
    pattern_searched_file = r'^produkt.*'
    start = None
    end = None
    path_choices = ''
    path = ''
    times = []
    response = None

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
        self.start = util.deserialize_datetime(start)
        self.end =  util.deserialize_datetime(end)
        self.path_choices = FtpFileFinder().findFile(self.generateWalkPathByResolutionAndStationId(),
                                                     r'.*' + self.stationId + '.*', r'^Meta_Daten.*')
        self.response = Response()
        self.response.observation_type = self.observation_type
        self.response.resolution = self.resolution
        self.response.station_id = self.stationId
        self.response.timeseries = []

    def generateWalkPathByResolutionAndStationId(self):
        """
        add the resolution and the observation type to the path
        :return: String
        """
        return PATH_TO_WALK + self.resolution + "/" + self.observation_type

    def zip_extract(self, half_path):
        """
        unpacking a single zip file for a path.
        returns a dictionary sorted by records
        :param half_path: string
        :return: Dictionary
        """

        self.path = "ftp://" + DWD_SERVER + "/" + half_path

        mysock = urllib.request.urlopen(self.path)

        memfile = io.BytesIO(mysock.read())

        with ZipFile(memfile, 'r') as myzip:

            nameList = myzip.namelist()
            p = re.compile(self.pattern_searched_file)

            for name in nameList:
                m = p.match(name)
                if m:
                    filename = m.group()
            f = myzip.open(filename)
            csv_read = pd.read_csv(f, sep = ";")  # read as DataFrame
            start_date = csv_read['MESS_DATUM'][0]  # get the start date of CSV
            end_date = csv_read['MESS_DATUM'][-1:].values  # get end date of CSV
            dict_date = dict(start = start_date, end = end_date[0])

            self.times.append(dict_date)

        return csv_read

    def dwd_response(self):

        """
        concat the different CSV's and reform the respond Object to but Meta Data on  the top of each
        row.
        :return: Dictionary
        """

        for single_path in self.path_choices:  # Loop over path path choices to look over

            r_dict = self.zip_extract(single_path)
            path_split = single_path.split('/')
            file_name = path_split[-1]
            epoch = path_split[-2]

            self.extract_timestamps(epoch, file_name, r_dict)

        return self.response


    def extract_timestamps(self, epoch, file_name, r_dict):
        if epoch in ['recent', 'now']  :  # remove redundancy (the Data from 'historical' comes at first )
            list_of_dicts = r_dict[r_dict['MESS_DATUM'] > int(self.times[0]['end'])].to_dict('records')

        else:
            list_of_dicts = r_dict.to_dict('records')
            # loop over the dictionary to delete the unused column &  reorganize the TimeSeries
        for i, single_dict in enumerate(list_of_dicts, 2):
            single_dict.pop('STATIONS_ID', None)
            single_dict.pop('eor', None)
            single_dict['timestamp'] = util.deserialize_datetime(str(decimal.Decimal(single_dict['MESS_DATUM'])))
            single_dict.pop('MESS_DATUM', None)
            timestamp = pytz.utc.localize(single_dict['timestamp'])  # type: datetime
            if (self.start <= timestamp) and (timestamp <= self.end):
                self.extract_timestamp(epoch, file_name, i, single_dict)


    def extract_timestamp(self, epoch, file_name, source_line_number, single_dict):
        ts = ResponseTimeseries()
        ts.epoch = epoch
        ts.source_line = source_line_number
        ts.source_file = file_name
        ts.source_url = self.path
        ts.values = []
        for k, v in single_dict.items():

            if k != 'timestamp':
                ts.values.append(Values(name = k, value = v))
            else:
                ts.timestamp = v
        self.response.timeseries.append(ts)
