# coding: utf-8

"""
    Veeam Backup for Nutanix AHV REST API 4.0

    This REST API reference lists types of Veeam Backup for Nutanix AHV entities,  and contains description of collections and resources which stand for these entities.  Every resource has a JSON object model and includes application data and REST API metadata.  Application data is represented by properties associated with Veeam Backup for Nutanix AHV entities.  REST API metadata is represented by properties specific to the REST API, such as resource IDs, URLs and relationships.  The reference also includes methods that represent operations available to a resource or collection.   # noqa: E501

    OpenAPI spec version: V4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.service_settings_api import ServiceSettingsApi  # noqa: E501
from swagger_client.rest import ApiException


class TestServiceSettingsApi(unittest.TestCase):
    """ServiceSettingsApi unit test stubs"""

    def setUp(self):
        self.api = ServiceSettingsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_service_settings_get_network_settings(self):
        """Test case for service_settings_get_network_settings

        Get Backup Appliance Network Settings  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()