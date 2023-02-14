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

class GfsYearlySettings(object):
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
        'enabled': 'bool',
        'yearly_retention': 'int',
        'month': 'Month'
    }

    attribute_map = {
        'enabled': 'enabled',
        'yearly_retention': 'yearlyRetention',
        'month': 'month'
    }

    def __init__(self, enabled=None, yearly_retention=None, month=None):  # noqa: E501
        """GfsYearlySettings - a model defined in Swagger"""  # noqa: E501
        self._enabled = None
        self._yearly_retention = None
        self._month = None
        self.discriminator = None
        if enabled is not None:
            self.enabled = enabled
        if yearly_retention is not None:
            self.yearly_retention = yearly_retention
        if month is not None:
            self.month = month

    @property
    def enabled(self):
        """Gets the enabled of this GfsYearlySettings.  # noqa: E501

        Defines whether creating yearly GFS backups is enabled in the job.  # noqa: E501

        :return: The enabled of this GfsYearlySettings.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this GfsYearlySettings.

        Defines whether creating yearly GFS backups is enabled in the job.  # noqa: E501

        :param enabled: The enabled of this GfsYearlySettings.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def yearly_retention(self):
        """Gets the yearly_retention of this GfsYearlySettings.  # noqa: E501


        :return: The yearly_retention of this GfsYearlySettings.  # noqa: E501
        :rtype: int
        """
        return self._yearly_retention

    @yearly_retention.setter
    def yearly_retention(self, yearly_retention):
        """Sets the yearly_retention of this GfsYearlySettings.


        :param yearly_retention: The yearly_retention of this GfsYearlySettings.  # noqa: E501
        :type: int
        """

        self._yearly_retention = yearly_retention

    @property
    def month(self):
        """Gets the month of this GfsYearlySettings.  # noqa: E501


        :return: The month of this GfsYearlySettings.  # noqa: E501
        :rtype: Month
        """
        return self._month

    @month.setter
    def month(self, month):
        """Sets the month of this GfsYearlySettings.


        :param month: The month of this GfsYearlySettings.  # noqa: E501
        :type: Month
        """

        self._month = month

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
        if issubclass(GfsYearlySettings, dict):
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
        if not isinstance(other, GfsYearlySettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other