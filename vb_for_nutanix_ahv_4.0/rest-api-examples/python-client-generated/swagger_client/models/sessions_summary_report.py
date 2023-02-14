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

class SessionsSummaryReport(object):
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
        'sessions_error': 'int',
        'sessions_error_difference': 'SummaryCountDifference',
        'sessions_warning': 'int',
        'sessions_warning_difference': 'SummaryCountDifference',
        'sessions_success': 'int',
        'sessions_success_difference': 'SummaryCountDifference',
        'sessions_running': 'int',
        'sessions_running_difference': 'SummaryCountDifference'
    }

    attribute_map = {
        'sessions_error': 'sessionsError',
        'sessions_error_difference': 'sessionsErrorDifference',
        'sessions_warning': 'sessionsWarning',
        'sessions_warning_difference': 'sessionsWarningDifference',
        'sessions_success': 'sessionsSuccess',
        'sessions_success_difference': 'sessionsSuccessDifference',
        'sessions_running': 'sessionsRunning',
        'sessions_running_difference': 'sessionsRunningDifference'
    }

    def __init__(self, sessions_error=None, sessions_error_difference=None, sessions_warning=None, sessions_warning_difference=None, sessions_success=None, sessions_success_difference=None, sessions_running=None, sessions_running_difference=None):  # noqa: E501
        """SessionsSummaryReport - a model defined in Swagger"""  # noqa: E501
        self._sessions_error = None
        self._sessions_error_difference = None
        self._sessions_warning = None
        self._sessions_warning_difference = None
        self._sessions_success = None
        self._sessions_success_difference = None
        self._sessions_running = None
        self._sessions_running_difference = None
        self.discriminator = None
        self.sessions_error = sessions_error
        self.sessions_error_difference = sessions_error_difference
        self.sessions_warning = sessions_warning
        self.sessions_warning_difference = sessions_warning_difference
        self.sessions_success = sessions_success
        self.sessions_success_difference = sessions_success_difference
        self.sessions_running = sessions_running
        self.sessions_running_difference = sessions_running_difference

    @property
    def sessions_error(self):
        """Gets the sessions_error of this SessionsSummaryReport.  # noqa: E501

        Number of sessions completed with errors.  # noqa: E501

        :return: The sessions_error of this SessionsSummaryReport.  # noqa: E501
        :rtype: int
        """
        return self._sessions_error

    @sessions_error.setter
    def sessions_error(self, sessions_error):
        """Sets the sessions_error of this SessionsSummaryReport.

        Number of sessions completed with errors.  # noqa: E501

        :param sessions_error: The sessions_error of this SessionsSummaryReport.  # noqa: E501
        :type: int
        """
        if sessions_error is None:
            raise ValueError("Invalid value for `sessions_error`, must not be `None`")  # noqa: E501

        self._sessions_error = sessions_error

    @property
    def sessions_error_difference(self):
        """Gets the sessions_error_difference of this SessionsSummaryReport.  # noqa: E501


        :return: The sessions_error_difference of this SessionsSummaryReport.  # noqa: E501
        :rtype: SummaryCountDifference
        """
        return self._sessions_error_difference

    @sessions_error_difference.setter
    def sessions_error_difference(self, sessions_error_difference):
        """Sets the sessions_error_difference of this SessionsSummaryReport.


        :param sessions_error_difference: The sessions_error_difference of this SessionsSummaryReport.  # noqa: E501
        :type: SummaryCountDifference
        """
        if sessions_error_difference is None:
            raise ValueError("Invalid value for `sessions_error_difference`, must not be `None`")  # noqa: E501

        self._sessions_error_difference = sessions_error_difference

    @property
    def sessions_warning(self):
        """Gets the sessions_warning of this SessionsSummaryReport.  # noqa: E501

        Number of sessions completed with warning.  # noqa: E501

        :return: The sessions_warning of this SessionsSummaryReport.  # noqa: E501
        :rtype: int
        """
        return self._sessions_warning

    @sessions_warning.setter
    def sessions_warning(self, sessions_warning):
        """Sets the sessions_warning of this SessionsSummaryReport.

        Number of sessions completed with warning.  # noqa: E501

        :param sessions_warning: The sessions_warning of this SessionsSummaryReport.  # noqa: E501
        :type: int
        """
        if sessions_warning is None:
            raise ValueError("Invalid value for `sessions_warning`, must not be `None`")  # noqa: E501

        self._sessions_warning = sessions_warning

    @property
    def sessions_warning_difference(self):
        """Gets the sessions_warning_difference of this SessionsSummaryReport.  # noqa: E501


        :return: The sessions_warning_difference of this SessionsSummaryReport.  # noqa: E501
        :rtype: SummaryCountDifference
        """
        return self._sessions_warning_difference

    @sessions_warning_difference.setter
    def sessions_warning_difference(self, sessions_warning_difference):
        """Sets the sessions_warning_difference of this SessionsSummaryReport.


        :param sessions_warning_difference: The sessions_warning_difference of this SessionsSummaryReport.  # noqa: E501
        :type: SummaryCountDifference
        """
        if sessions_warning_difference is None:
            raise ValueError("Invalid value for `sessions_warning_difference`, must not be `None`")  # noqa: E501

        self._sessions_warning_difference = sessions_warning_difference

    @property
    def sessions_success(self):
        """Gets the sessions_success of this SessionsSummaryReport.  # noqa: E501

        Number of successfully completed sessions.  # noqa: E501

        :return: The sessions_success of this SessionsSummaryReport.  # noqa: E501
        :rtype: int
        """
        return self._sessions_success

    @sessions_success.setter
    def sessions_success(self, sessions_success):
        """Sets the sessions_success of this SessionsSummaryReport.

        Number of successfully completed sessions.  # noqa: E501

        :param sessions_success: The sessions_success of this SessionsSummaryReport.  # noqa: E501
        :type: int
        """
        if sessions_success is None:
            raise ValueError("Invalid value for `sessions_success`, must not be `None`")  # noqa: E501

        self._sessions_success = sessions_success

    @property
    def sessions_success_difference(self):
        """Gets the sessions_success_difference of this SessionsSummaryReport.  # noqa: E501


        :return: The sessions_success_difference of this SessionsSummaryReport.  # noqa: E501
        :rtype: SummaryCountDifference
        """
        return self._sessions_success_difference

    @sessions_success_difference.setter
    def sessions_success_difference(self, sessions_success_difference):
        """Sets the sessions_success_difference of this SessionsSummaryReport.


        :param sessions_success_difference: The sessions_success_difference of this SessionsSummaryReport.  # noqa: E501
        :type: SummaryCountDifference
        """
        if sessions_success_difference is None:
            raise ValueError("Invalid value for `sessions_success_difference`, must not be `None`")  # noqa: E501

        self._sessions_success_difference = sessions_success_difference

    @property
    def sessions_running(self):
        """Gets the sessions_running of this SessionsSummaryReport.  # noqa: E501

        Number of running sessions.  # noqa: E501

        :return: The sessions_running of this SessionsSummaryReport.  # noqa: E501
        :rtype: int
        """
        return self._sessions_running

    @sessions_running.setter
    def sessions_running(self, sessions_running):
        """Sets the sessions_running of this SessionsSummaryReport.

        Number of running sessions.  # noqa: E501

        :param sessions_running: The sessions_running of this SessionsSummaryReport.  # noqa: E501
        :type: int
        """
        if sessions_running is None:
            raise ValueError("Invalid value for `sessions_running`, must not be `None`")  # noqa: E501

        self._sessions_running = sessions_running

    @property
    def sessions_running_difference(self):
        """Gets the sessions_running_difference of this SessionsSummaryReport.  # noqa: E501


        :return: The sessions_running_difference of this SessionsSummaryReport.  # noqa: E501
        :rtype: SummaryCountDifference
        """
        return self._sessions_running_difference

    @sessions_running_difference.setter
    def sessions_running_difference(self, sessions_running_difference):
        """Sets the sessions_running_difference of this SessionsSummaryReport.


        :param sessions_running_difference: The sessions_running_difference of this SessionsSummaryReport.  # noqa: E501
        :type: SummaryCountDifference
        """
        if sessions_running_difference is None:
            raise ValueError("Invalid value for `sessions_running_difference`, must not be `None`")  # noqa: E501

        self._sessions_running_difference = sessions_running_difference

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
        if issubclass(SessionsSummaryReport, dict):
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
        if not isinstance(other, SessionsSummaryReport):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other