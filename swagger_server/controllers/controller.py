import datetime

import connexion
import six

from swagger_server.models import Values, InlineResponse2001Timeseries
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.dwd_response import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server import util


def capabilities_station_id_get(stationId):  # noqa: E501
    """capabilities_station_id_get

    Query the capabilities of a specific station by its station ID. # noqa: E501

    :param stationId: The DWD station id derived from [list](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_list_soil.txt) or [map](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_map_soil.png) 
    :type stationId: str

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def timeseries_station_id_resolution_observation_type_get(stationId, resolution, observation_type, start=None, end=None):  # noqa: E501
    """timeseries_station_id_resolution_observation_type_get

    Query the DWD FTP service by a specified station, resolution and datatype and a optional timerange # noqa: E501

    :param stationId: The DWD station id derived from [list](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_list_soil.txt) or [map](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_map_soil.png) 
    :type stationId: str
    :param resolution: The resolution which should be queried 
    :type resolution: str
    :param obeservation_type: The type of observeation which should be queried 
    :type obeservation_type: str
    :param start: Start of the timerange to query
    :type start: str
    :param end: End of the time range to query
    :type end: str

    :rtype: InlineResponse2001
    """

    if start is None:
        start = '01.01.{0:04d} 00:00:00'.format(datetime.MINYEAR)

    if end is None:
        end = '31.12.{0:04d} 23:59:59'.format(datetime.MAXYEAR)

    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)

    resp = InlineResponse2001(station_id=stationId, resolution=resolution,
                              observation_type=observation_type)  # type: InlineResponse2001

    ts = InlineResponse2001Timeseries(
        timestamp=datetime.datetime.now(),
        epoch='recent',
        source_file='foo.csv',
        source_url='ftp://example.com/foo.zip',
        source_line=23
    )

    ts.values = [
        Values(name='QN', value=3),
        Values(name='PP_10', value=-999),
        Values(name='TT_10', value=13.2),
        Values(name='TM5_10', value=14.9),
        Values(name='RF_10', value=75.9),
        Values(name='TD_10', value=9.0),
    ]

    resp.timeseries = [ts]

    return resp
