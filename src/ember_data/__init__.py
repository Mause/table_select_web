from .base_rest_endpoint import BaseRESTEndpoint
BaseRESTEndpoint


def record_check(func):
    func.__record_checker__ = True
    return func
