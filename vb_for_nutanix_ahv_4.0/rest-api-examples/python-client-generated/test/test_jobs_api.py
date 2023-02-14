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
from swagger_client.api.jobs_api import JobsApi  # noqa: E501
from swagger_client.rest import ApiException


class TestJobsApi(unittest.TestCase):
    """JobsApi unit test stubs"""

    def setUp(self):
        self.api = JobsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_jobs_add(self):
        """Test case for jobs_add

        Create Backup job  # noqa: E501
        """
        pass

    def test_jobs_delete(self):
        """Test case for jobs_delete

        Delete Job  # noqa: E501
        """
        pass

    def test_jobs_disable(self):
        """Test case for jobs_disable

        Disable Job  # noqa: E501
        """
        pass

    def test_jobs_enable(self):
        """Test case for jobs_enable

        Enable Job  # noqa: E501
        """
        pass

    def test_jobs_get_by_id(self):
        """Test case for jobs_get_by_id

        Get Job Data  # noqa: E501
        """
        pass

    def test_jobs_get_page(self):
        """Test case for jobs_get_page

        Get Collection of Jobs  # noqa: E501
        """
        pass

    def test_jobs_get_settings(self):
        """Test case for jobs_get_settings

        Get Job Setting  # noqa: E501
        """
        pass

    def test_jobs_start(self):
        """Test case for jobs_start

        Starts Job  # noqa: E501
        """
        pass

    def test_jobs_stop(self):
        """Test case for jobs_stop

        Stop Job  # noqa: E501
        """
        pass

    def test_jobs_update_settings(self):
        """Test case for jobs_update_settings

        Modify Job Settings  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()