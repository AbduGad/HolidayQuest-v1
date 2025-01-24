# -*- coding: utf-8 -*-
import sys

import six

from collections import OrderedDict


if six.PY3:  # pragma: no branch
    from inspect import signature
else:
    from funcsigs import signature

from boltons.funcutils import wraps
from six import string_types


class GuardError(Exception):
    pass


def _params(f, argumets, keyword_argumets, params):
    sig = signature(f)
    bind = sig.bind(*argumets, **keyword_argumets)
    if sys.version_info >= (3, 5):
        bind.apply_defaults()

    return OrderedDict(
        filter(
            lambda item: item[0] in params,
            bind.arguments.items()
        )
    )


def guard(params, guardian, error_class=GuardError, message=''):
    '''
    A guard function - check parameters
    with guardian function on decorated function

    :param tuple or string params: guarded function parameter/s
    :param function guardian: verifying the conditions for the selected parameter
    :param Exception error_class: raised class when guardian return false
    :param string message: error message
    '''
    params = [params] if isinstance(params, string_types) else params

    def guard_decorate(f):
        @wraps(f)
        def _guard_decorate(*args, **kwargs):
            if guardian(**_params(f, args, kwargs, params)):
                return f(*args, **kwargs)
            else:
                raise error_class(message)
        return _guard_decorate
    return guard_decorate
