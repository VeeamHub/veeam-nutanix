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

class SessionProgressState(object):
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
        'events': 'list[ProgressEvent]',
        'transferred': 'DataValue',
        'read': 'DataValue',
        'processed': 'DataValue',
        'progress_percents': 'int',
        'processing_rate': 'int',
        'avg_processing_rate': 'int',
        'is_processing_rate_supported': 'bool',
        'objects_count': 'int',
        'objects_processed': 'int'
    }

    attribute_map = {
        'events': 'events',
        'transferred': 'transferred',
        'read': 'read',
        'processed': 'processed',
        'progress_percents': 'progressPercents',
        'processing_rate': 'processingRate',
        'avg_processing_rate': 'avgProcessingRate',
        'is_processing_rate_supported': 'isProcessingRateSupported',
        'objects_count': 'objectsCount',
        'objects_processed': 'objectsProcessed'
    }

    def __init__(self, events=None, transferred=None, read=None, processed=None, progress_percents=None, processing_rate=None, avg_processing_rate=None, is_processing_rate_supported=None, objects_count=None, objects_processed=None):  # noqa: E501
        """SessionProgressState - a model defined in Swagger"""  # noqa: E501
        self._events = None
        self._transferred = None
        self._read = None
        self._processed = None
        self._progress_percents = None
        self._processing_rate = None
        self._avg_processing_rate = None
        self._is_processing_rate_supported = None
        self._objects_count = None
        self._objects_processed = None
        self.discriminator = None
        if events is not None:
            self.events = events
        if transferred is not None:
            self.transferred = transferred
        if read is not None:
            self.read = read
        if processed is not None:
            self.processed = processed
        if progress_percents is not None:
            self.progress_percents = progress_percents
        if processing_rate is not None:
            self.processing_rate = processing_rate
        if avg_processing_rate is not None:
            self.avg_processing_rate = avg_processing_rate
        if is_processing_rate_supported is not None:
            self.is_processing_rate_supported = is_processing_rate_supported
        if objects_count is not None:
            self.objects_count = objects_count
        if objects_processed is not None:
            self.objects_processed = objects_processed

    @property
    def events(self):
        """Gets the events of this SessionProgressState.  # noqa: E501

        Tasks executed during the session.  # noqa: E501

        :return: The events of this SessionProgressState.  # noqa: E501
        :rtype: list[ProgressEvent]
        """
        return self._events

    @events.setter
    def events(self, events):
        """Sets the events of this SessionProgressState.

        Tasks executed during the session.  # noqa: E501

        :param events: The events of this SessionProgressState.  # noqa: E501
        :type: list[ProgressEvent]
        """

        self._events = events

    @property
    def transferred(self):
        """Gets the transferred of this SessionProgressState.  # noqa: E501


        :return: The transferred of this SessionProgressState.  # noqa: E501
        :rtype: DataValue
        """
        return self._transferred

    @transferred.setter
    def transferred(self, transferred):
        """Sets the transferred of this SessionProgressState.


        :param transferred: The transferred of this SessionProgressState.  # noqa: E501
        :type: DataValue
        """

        self._transferred = transferred

    @property
    def read(self):
        """Gets the read of this SessionProgressState.  # noqa: E501


        :return: The read of this SessionProgressState.  # noqa: E501
        :rtype: DataValue
        """
        return self._read

    @read.setter
    def read(self, read):
        """Sets the read of this SessionProgressState.


        :param read: The read of this SessionProgressState.  # noqa: E501
        :type: DataValue
        """

        self._read = read

    @property
    def processed(self):
        """Gets the processed of this SessionProgressState.  # noqa: E501


        :return: The processed of this SessionProgressState.  # noqa: E501
        :rtype: DataValue
        """
        return self._processed

    @processed.setter
    def processed(self, processed):
        """Sets the processed of this SessionProgressState.


        :param processed: The processed of this SessionProgressState.  # noqa: E501
        :type: DataValue
        """

        self._processed = processed

    @property
    def progress_percents(self):
        """Gets the progress_percents of this SessionProgressState.  # noqa: E501


        :return: The progress_percents of this SessionProgressState.  # noqa: E501
        :rtype: int
        """
        return self._progress_percents

    @progress_percents.setter
    def progress_percents(self, progress_percents):
        """Sets the progress_percents of this SessionProgressState.


        :param progress_percents: The progress_percents of this SessionProgressState.  # noqa: E501
        :type: int
        """

        self._progress_percents = progress_percents

    @property
    def processing_rate(self):
        """Gets the processing_rate of this SessionProgressState.  # noqa: E501


        :return: The processing_rate of this SessionProgressState.  # noqa: E501
        :rtype: int
        """
        return self._processing_rate

    @processing_rate.setter
    def processing_rate(self, processing_rate):
        """Sets the processing_rate of this SessionProgressState.


        :param processing_rate: The processing_rate of this SessionProgressState.  # noqa: E501
        :type: int
        """

        self._processing_rate = processing_rate

    @property
    def avg_processing_rate(self):
        """Gets the avg_processing_rate of this SessionProgressState.  # noqa: E501


        :return: The avg_processing_rate of this SessionProgressState.  # noqa: E501
        :rtype: int
        """
        return self._avg_processing_rate

    @avg_processing_rate.setter
    def avg_processing_rate(self, avg_processing_rate):
        """Sets the avg_processing_rate of this SessionProgressState.


        :param avg_processing_rate: The avg_processing_rate of this SessionProgressState.  # noqa: E501
        :type: int
        """

        self._avg_processing_rate = avg_processing_rate

    @property
    def is_processing_rate_supported(self):
        """Gets the is_processing_rate_supported of this SessionProgressState.  # noqa: E501


        :return: The is_processing_rate_supported of this SessionProgressState.  # noqa: E501
        :rtype: bool
        """
        return self._is_processing_rate_supported

    @is_processing_rate_supported.setter
    def is_processing_rate_supported(self, is_processing_rate_supported):
        """Sets the is_processing_rate_supported of this SessionProgressState.


        :param is_processing_rate_supported: The is_processing_rate_supported of this SessionProgressState.  # noqa: E501
        :type: bool
        """

        self._is_processing_rate_supported = is_processing_rate_supported

    @property
    def objects_count(self):
        """Gets the objects_count of this SessionProgressState.  # noqa: E501


        :return: The objects_count of this SessionProgressState.  # noqa: E501
        :rtype: int
        """
        return self._objects_count

    @objects_count.setter
    def objects_count(self, objects_count):
        """Sets the objects_count of this SessionProgressState.


        :param objects_count: The objects_count of this SessionProgressState.  # noqa: E501
        :type: int
        """

        self._objects_count = objects_count

    @property
    def objects_processed(self):
        """Gets the objects_processed of this SessionProgressState.  # noqa: E501


        :return: The objects_processed of this SessionProgressState.  # noqa: E501
        :rtype: int
        """
        return self._objects_processed

    @objects_processed.setter
    def objects_processed(self, objects_processed):
        """Sets the objects_processed of this SessionProgressState.


        :param objects_processed: The objects_processed of this SessionProgressState.  # noqa: E501
        :type: int
        """

        self._objects_processed = objects_processed

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
        if issubclass(SessionProgressState, dict):
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
        if not isinstance(other, SessionProgressState):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
