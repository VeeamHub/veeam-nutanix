# coding: utf-8

"""
    Veeam Backup for Nutanix AHV REST API 4.0

    This REST API reference lists types of Veeam Backup for Nutanix AHV entities,  and contains description of collections and resources which stand for these entities.  Every resource has a JSON object model and includes application data and REST API metadata.  Application data is represented by properties associated with Veeam Backup for Nutanix AHV entities.  REST API metadata is represented by properties specific to the REST API, such as resource IDs, URLs and relationships.  The reference also includes methods that represent operations available to a resource or collection.   # noqa: E501

    OpenAPI spec version: V4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TopJobsDurationReportItem(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'job_id': 'str',
        'job_mode': 'JobMode',
        'job_name': 'str',
        'start_time_utc': 'datetime',
        'duration': 'str',
        'duration_difference': 'str',
        'percentage': 'int'
    }

    attribute_map = {
        'job_id': 'jobId',
        'job_mode': 'jobMode',
        'job_name': 'jobName',
        'start_time_utc': 'startTimeUtc',
        'duration': 'duration',
        'duration_difference': 'durationDifference',
        'percentage': 'percentage'
    }

    def __init__(self, job_id=None, job_mode=None, job_name=None, start_time_utc=None, duration=None, duration_difference=None, percentage=None):  # noqa: E501
        """TopJobsDurationReportItem - a model defined in Swagger"""  # noqa: E501
        self._job_id = None
        self._job_mode = None
        self._job_name = None
        self._start_time_utc = None
        self._duration = None
        self._duration_difference = None
        self._percentage = None
        self.discriminator = None
        self.job_id = job_id
        if job_mode is not None:
            self.job_mode = job_mode
        self.job_name = job_name
        self.start_time_utc = start_time_utc
        self.duration = duration
        if duration_difference is not None:
            self.duration_difference = duration_difference
        if percentage is not None:
            self.percentage = percentage

    @property
    def job_id(self):
        """Gets the job_id of this TopJobsDurationReportItem.  # noqa: E501

        System ID assigned to a job in Veeam Backup for Nutanix AHV.  # noqa: E501

        :return: The job_id of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this TopJobsDurationReportItem.

        System ID assigned to a job in Veeam Backup for Nutanix AHV.  # noqa: E501

        :param job_id: The job_id of this TopJobsDurationReportItem.  # noqa: E501
        :type: str
        """
        if job_id is None:
            raise ValueError("Invalid value for `job_id`, must not be `None`")  # noqa: E501

        self._job_id = job_id

    @property
    def job_mode(self):
        """Gets the job_mode of this TopJobsDurationReportItem.  # noqa: E501


        :return: The job_mode of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: JobMode
        """
        return self._job_mode

    @job_mode.setter
    def job_mode(self, job_mode):
        """Sets the job_mode of this TopJobsDurationReportItem.


        :param job_mode: The job_mode of this TopJobsDurationReportItem.  # noqa: E501
        :type: JobMode
        """

        self._job_mode = job_mode

    @property
    def job_name(self):
        """Gets the job_name of this TopJobsDurationReportItem.  # noqa: E501

        Name of the job.  # noqa: E501

        :return: The job_name of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: str
        """
        return self._job_name

    @job_name.setter
    def job_name(self, job_name):
        """Sets the job_name of this TopJobsDurationReportItem.

        Name of the job.  # noqa: E501

        :param job_name: The job_name of this TopJobsDurationReportItem.  # noqa: E501
        :type: str
        """
        if job_name is None:
            raise ValueError("Invalid value for `job_name`, must not be `None`")  # noqa: E501

        self._job_name = job_name

    @property
    def start_time_utc(self):
        """Gets the start_time_utc of this TopJobsDurationReportItem.  # noqa: E501

        Date and time of the most recent job run.  # noqa: E501

        :return: The start_time_utc of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time_utc

    @start_time_utc.setter
    def start_time_utc(self, start_time_utc):
        """Sets the start_time_utc of this TopJobsDurationReportItem.

        Date and time of the most recent job run.  # noqa: E501

        :param start_time_utc: The start_time_utc of this TopJobsDurationReportItem.  # noqa: E501
        :type: datetime
        """
        if start_time_utc is None:
            raise ValueError("Invalid value for `start_time_utc`, must not be `None`")  # noqa: E501

        self._start_time_utc = start_time_utc

    @property
    def duration(self):
        """Gets the duration of this TopJobsDurationReportItem.  # noqa: E501

        Job session duration.  # noqa: E501

        :return: The duration of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: str
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this TopJobsDurationReportItem.

        Job session duration.  # noqa: E501

        :param duration: The duration of this TopJobsDurationReportItem.  # noqa: E501
        :type: str
        """
        if duration is None:
            raise ValueError("Invalid value for `duration`, must not be `None`")  # noqa: E501

        self._duration = duration

    @property
    def duration_difference(self):
        """Gets the duration_difference of this TopJobsDurationReportItem.  # noqa: E501

        Time span between the latest job session duration and the average duration of the last 10 successful sessions of the job.  # noqa: E501

        :return: The duration_difference of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: str
        """
        return self._duration_difference

    @duration_difference.setter
    def duration_difference(self, duration_difference):
        """Sets the duration_difference of this TopJobsDurationReportItem.

        Time span between the latest job session duration and the average duration of the last 10 successful sessions of the job.  # noqa: E501

        :param duration_difference: The duration_difference of this TopJobsDurationReportItem.  # noqa: E501
        :type: str
        """

        self._duration_difference = duration_difference

    @property
    def percentage(self):
        """Gets the percentage of this TopJobsDurationReportItem.  # noqa: E501

        Difference between the latest job session duration and the average duration of the last 10 successful sessions of the job (in percent).  # noqa: E501

        :return: The percentage of this TopJobsDurationReportItem.  # noqa: E501
        :rtype: int
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """Sets the percentage of this TopJobsDurationReportItem.

        Difference between the latest job session duration and the average duration of the last 10 successful sessions of the job (in percent).  # noqa: E501

        :param percentage: The percentage of this TopJobsDurationReportItem.  # noqa: E501
        :type: int
        """

        self._percentage = percentage

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TopJobsDurationReportItem, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TopJobsDurationReportItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
