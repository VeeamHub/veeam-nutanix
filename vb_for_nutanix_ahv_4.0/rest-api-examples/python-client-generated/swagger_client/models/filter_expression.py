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

class FilterExpression(object):
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
        '_property': 'str',
        'items': 'list[FilterExpression]',
        'operation': 'str',
        'collation': 'Collation',
        'value': 'object'
    }

    attribute_map = {
        '_property': 'property',
        'items': 'items',
        'operation': 'operation',
        'collation': 'collation',
        'value': 'value'
    }

    def __init__(self, _property=None, items=None, operation=None, collation=None, value=None):  # noqa: E501
        """FilterExpression - a model defined in Swagger"""  # noqa: E501
        self.__property = None
        self._items = None
        self._operation = None
        self._collation = None
        self._value = None
        self.discriminator = None
        if _property is not None:
            self._property = _property
        if items is not None:
            self.items = items
        self.operation = operation
        if collation is not None:
            self.collation = collation
        if value is not None:
            self.value = value

    @property
    def _property(self):
        """Gets the _property of this FilterExpression.  # noqa: E501

        Path to the required resource property.  # noqa: E501

        :return: The _property of this FilterExpression.  # noqa: E501
        :rtype: str
        """
        return self.__property

    @_property.setter
    def _property(self, _property):
        """Sets the _property of this FilterExpression.

        Path to the required resource property.  # noqa: E501

        :param _property: The _property of this FilterExpression.  # noqa: E501
        :type: str
        """

        self.__property = _property

    @property
    def items(self):
        """Gets the items of this FilterExpression.  # noqa: E501

        Inner expressions. Can be used only with `and`, `or` and `not` operation.  # noqa: E501

        :return: The items of this FilterExpression.  # noqa: E501
        :rtype: list[FilterExpression]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this FilterExpression.

        Inner expressions. Can be used only with `and`, `or` and `not` operation.  # noqa: E501

        :param items: The items of this FilterExpression.  # noqa: E501
        :type: list[FilterExpression]
        """

        self._items = items

    @property
    def operation(self):
        """Gets the operation of this FilterExpression.  # noqa: E501

        Filter operation.  # noqa: E501

        :return: The operation of this FilterExpression.  # noqa: E501
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this FilterExpression.

        Filter operation.  # noqa: E501

        :param operation: The operation of this FilterExpression.  # noqa: E501
        :type: str
        """
        if operation is None:
            raise ValueError("Invalid value for `operation`, must not be `None`")  # noqa: E501
        allowed_values = ["In", "Contains", "Subset", "Superset", "Equals", "NotEquals", "LessThan", "LessThanOrEqual", "GreaterThan", "GreaterThanOrEqual", "ExclusiveOr", "Or", "And", "Not"]  # noqa: E501
        if operation not in allowed_values:
            raise ValueError(
                "Invalid value for `operation` ({0}), must be one of {1}"  # noqa: E501
                .format(operation, allowed_values)
            )

        self._operation = operation

    @property
    def collation(self):
        """Gets the collation of this FilterExpression.  # noqa: E501


        :return: The collation of this FilterExpression.  # noqa: E501
        :rtype: Collation
        """
        return self._collation

    @collation.setter
    def collation(self, collation):
        """Sets the collation of this FilterExpression.


        :param collation: The collation of this FilterExpression.  # noqa: E501
        :type: Collation
        """

        self._collation = collation

    @property
    def value(self):
        """Gets the value of this FilterExpression.  # noqa: E501

        Resource property value.  # noqa: E501

        :return: The value of this FilterExpression.  # noqa: E501
        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this FilterExpression.

        Resource property value.  # noqa: E501

        :param value: The value of this FilterExpression.  # noqa: E501
        :type: object
        """

        self._value = value

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
        if issubclass(FilterExpression, dict):
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
        if not isinstance(other, FilterExpression):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
