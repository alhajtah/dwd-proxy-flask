# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.dwd_response import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_capabilities_station_id_get(self):
        """Test case for capabilities_station_id_get

        
        """
        response = self.client.open(
            '//capabilities/{stationId}'.format(stationId='stationId_example'),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_timeseries_station_id_resolution_observation_type_get(self):
        """Test case for timeseries_station_id_resolution_observation_type_get

        
        """
        query_string = [('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '//timeseries/{stationId}/{resolution}/{observation_type}'.format(stationId='stationId_example', resolution='resolution_example', obeservation_type='obeservation_type_example'),
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
