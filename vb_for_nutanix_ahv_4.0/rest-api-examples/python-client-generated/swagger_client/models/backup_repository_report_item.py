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

class BackupRepositoryReportItem(object):
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
        'id': 'str',
        'name': 'str',
        'total_space': 'int',
        'free_space': 'int',
        'used_space': 'int',
        'status': 'BackupRepositorySpaceStatus'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'total_space': 'totalSpace',
        'free_space': 'freeSpace',
        'used_space': 'usedSpace',
        'status': 'status'
    }

    def __init__(self, id=None, name=None, total_space=None, free_space=None, used_space=None, status=None):  # noqa: E501
        """BackupRepositoryReportItem - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._total_space = None
        self._free_space = None
        self._used_space = None
        self._status = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if total_space is not None:
            self.total_space = total_space
        if free_space is not None:
            self.free_space = free_space
        if used_space is not None:
            self.used_space = used_space
        self.status = status

    @property
    def id(self):
        """Gets the id of this BackupRepositoryReportItem.  # noqa: E501

        System ID assigned to a backup repository in Veeam Backup for Nutanix AHV.  # noqa: E501

        :return: The id of this BackupRepositoryReportItem.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BackupRepositoryReportItem.

        System ID assigned to a backup repository in Veeam Backup for Nutanix AHV.  # noqa: E501

        :param id: The id of this BackupRepositoryReportItem.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this BackupRepositoryReportItem.  # noqa: E501

        Name of the backup repository in Veeam Backup for Nutanix AHV.  # noqa: E501

        :return: The name of this BackupRepositoryReportItem.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this BackupRepositoryReportItem.

        Name of the backup repository in Veeam Backup for Nutanix AHV.  # noqa: E501

        :param name: The name of this BackupRepositoryReportItem.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def total_space(self):
        """Gets the total_space of this BackupRepositoryReportItem.  # noqa: E501

        Total capacity of the backup repository (in bytes).  # noqa: E501

        :return: The total_space of this BackupRepositoryReportItem.  # noqa: E501
        :rtype: int
        """
        return self._total_space

    @total_space.setter
    def total_space(self, total_space):
        """Sets the total_space of this BackupRepositoryReportItem.

        Total capacity of the backup repository (in bytes).  # noqa: E501

        :param total_space: The total_space of this BackupRepositoryReportItem.  # noqa: E501
        :type: int
        """

        self._total_space = total_space

    @property
    def free_space(self):
        """Gets the free_space of this BackupRepositoryReportItem.  # noqa: E501

        Free space in the backup repository (in bytes).  # noqa: E501

        :return: The free_space of this BackupRepositoryReportItem.  # noqa: E501
        :rtype: int
        """
        return self._free_space

    @free_space.setter
    def free_space(self, free_space):
        """Sets the free_space of this BackupRepositoryReportItem.

        Free space in the backup repository (in bytes).  # noqa: E501

        :param free_space: The free_space of this BackupRepositoryReportItem.  # noqa: E501
        :type: int
        """

        self._free_space = free_space

    @property
    def used_space(self):
        """Gets the used_space of this BackupRepositoryReportItem.  # noqa: E501

        Used space in the backup repository (in bytes).  # noqa: E501

        :return: The used_space of this BackupRepositoryReportItem.  # noqa: E501
        :rtype: int
        """
        return self._used_space

    @used_space.setter
    def used_space(self, used_space):
        """Sets the used_space of this BackupRepositoryReportItem.

        Used space in the backup repository (in bytes).  # noqa: E501

        :param used_space: The used_space of this BackupRepositoryReportItem.  # noqa: E501
        :type: int
        """

        self._used_space = used_space

    @property
    def status(self):
        """Gets the status of this BackupRepositoryReportItem.  # noqa: E501


        :return: The status of this BackupRepositoryReportItem.  # noqa: E501
        :rtype: BackupRepositorySpaceStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this BackupRepositoryReportItem.


        :param status: The status of this BackupRepositoryReportItem.  # noqa: E501
        :type: BackupRepositorySpaceStatus
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

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
        if issubclass(BackupRepositoryReportItem, dict):
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
        if not isinstance(other, BackupRepositoryReportItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
