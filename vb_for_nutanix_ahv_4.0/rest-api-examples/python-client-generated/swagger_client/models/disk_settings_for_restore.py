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

class DiskSettingsForRestore(object):
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
        'disk_id': 'str',
        'bus_type': 'AhvBusType',
        'index': 'int',
        'storage_container_id': 'str'
    }

    attribute_map = {
        'disk_id': 'diskId',
        'bus_type': 'busType',
        'index': 'index',
        'storage_container_id': 'storageContainerId'
    }

    def __init__(self, disk_id=None, bus_type=None, index=None, storage_container_id=None):  # noqa: E501
        """DiskSettingsForRestore - a model defined in Swagger"""  # noqa: E501
        self._disk_id = None
        self._bus_type = None
        self._index = None
        self._storage_container_id = None
        self.discriminator = None
        self.disk_id = disk_id
        self.bus_type = bus_type
        self.index = index
        if storage_container_id is not None:
            self.storage_container_id = storage_container_id

    @property
    def disk_id(self):
        """Gets the disk_id of this DiskSettingsForRestore.  # noqa: E501

        ID assigned to a disk in the Nutanix AHV environment.  # noqa: E501

        :return: The disk_id of this DiskSettingsForRestore.  # noqa: E501
        :rtype: str
        """
        return self._disk_id

    @disk_id.setter
    def disk_id(self, disk_id):
        """Sets the disk_id of this DiskSettingsForRestore.

        ID assigned to a disk in the Nutanix AHV environment.  # noqa: E501

        :param disk_id: The disk_id of this DiskSettingsForRestore.  # noqa: E501
        :type: str
        """
        if disk_id is None:
            raise ValueError("Invalid value for `disk_id`, must not be `None`")  # noqa: E501

        self._disk_id = disk_id

    @property
    def bus_type(self):
        """Gets the bus_type of this DiskSettingsForRestore.  # noqa: E501


        :return: The bus_type of this DiskSettingsForRestore.  # noqa: E501
        :rtype: AhvBusType
        """
        return self._bus_type

    @bus_type.setter
    def bus_type(self, bus_type):
        """Sets the bus_type of this DiskSettingsForRestore.


        :param bus_type: The bus_type of this DiskSettingsForRestore.  # noqa: E501
        :type: AhvBusType
        """
        if bus_type is None:
            raise ValueError("Invalid value for `bus_type`, must not be `None`")  # noqa: E501

        self._bus_type = bus_type

    @property
    def index(self):
        """Gets the index of this DiskSettingsForRestore.  # noqa: E501

        Index of the VM virtual node to which the disk is connected.  # noqa: E501

        :return: The index of this DiskSettingsForRestore.  # noqa: E501
        :rtype: int
        """
        return self._index

    @index.setter
    def index(self, index):
        """Sets the index of this DiskSettingsForRestore.

        Index of the VM virtual node to which the disk is connected.  # noqa: E501

        :param index: The index of this DiskSettingsForRestore.  # noqa: E501
        :type: int
        """
        if index is None:
            raise ValueError("Invalid value for `index`, must not be `None`")  # noqa: E501

        self._index = index

    @property
    def storage_container_id(self):
        """Gets the storage_container_id of this DiskSettingsForRestore.  # noqa: E501

        ID of the storage container where the disk is located.  # noqa: E501

        :return: The storage_container_id of this DiskSettingsForRestore.  # noqa: E501
        :rtype: str
        """
        return self._storage_container_id

    @storage_container_id.setter
    def storage_container_id(self, storage_container_id):
        """Sets the storage_container_id of this DiskSettingsForRestore.

        ID of the storage container where the disk is located.  # noqa: E501

        :param storage_container_id: The storage_container_id of this DiskSettingsForRestore.  # noqa: E501
        :type: str
        """

        self._storage_container_id = storage_container_id

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
        if issubclass(DiskSettingsForRestore, dict):
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
        if not isinstance(other, DiskSettingsForRestore):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
