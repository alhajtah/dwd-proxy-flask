# coding: utf-8

from __future__ import absolute_import

from app.test import BaseTestCase


class TestController(BaseTestCase):
    """Controller integration test stubs"""

    def test_capabilities_station_id_get(self):
        """Test case for capabilities_station_id_get

        
        """
        response = self.client.open(
            '{HOST}/capabilities/{stationId}'.format(HOST='localhost:8080',stationId='stationId_example'),
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
            '{HOST}/timeseries/{stationId}/{resolution}/{observation_type}'.format(HOST='localhost:8080',
                                                                                   stationId='stationId_example',
                                                                              resolution='resolution_example',
                                                                              obeservation_type='obeservation_type_example'),
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
