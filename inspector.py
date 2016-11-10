# @Time    : 2016/11/10 12:01
# @Author  : Zhang Chen
# @Email    : zhangchen.shaanxi@gmail.com
# @File    : inspector.py


# Exception types
#
class InspectorException(Exception):
    def __init__(self, message=None):
        super(InspectorException, self).__init__(message)


class InstanceNotFoundException(InspectorException):
    pass


class InstanceShutOffException(InspectorException):
    pass


class InstanceNoDataException(InspectorException):
    pass


class NoDataException(InspectorException):
    pass


class NoSanityException(InspectorException):
    pass