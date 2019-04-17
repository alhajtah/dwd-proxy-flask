import datetime

from dwd_code.capabilities import Capabilities
from dwd_code.timeseries import TimeSeries
from swagger_server.models.dwd_response import Response  # noqa: E501


def capabilities_station_id_get(stationId):  # noqa: E501
    """capabilities_station_id_get

    Query the capabilities of a specific station by its station ID. # noqa: E501

    :param stationId: The DWD station id derived from [list](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_list_soil.txt) or [map](ftp://ftp-cdc.dwd.de/pub/CDC/help/stations_map_soil.png) 
    :type stationId: str

    :rtype: InlineResponse200
    """
    c = Capabilities(stationId)
    dict = c.get_capabilities_by_station_id( )

    return dict


def timeseries_station_id_resolution_observation_type_get(stationId, resolution, observation_type,
                                                          start='01.01.{0:04d} 00:00:00Z'.format(datetime.MINYEAR),
                                                          end='31.12.{0:04d} 23:59:59Z'.format(
                                                              datetime.MAXYEAR)):  # noqa: E501
    """

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

    :rtype: Response
    """


    p = TimeSeries(stationId = stationId, resolution = resolution,
                   observation_type = observation_type, start = start, end = end).dwd_response( )

    return p
