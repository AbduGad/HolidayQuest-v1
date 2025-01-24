# -*- coding: utf-8 -*-

from toolz import compose as c


def prepare(fn):
    def _prepare(*args, **kwargs):
        try:
            return (fn(*args, **kwargs), None)
        except Exception as e:
            return (None, e)

    return _prepare


def catch(error, fn):
    def _catch(container):
        data, excp = container

        if isinstance(excp, error):
            return (fn(excp), None)
        else:
            return container

    return _catch


def get_or_reraise(container):
    data, excp = container

    if excp is None:
        return data
    else:
        raise excp


def compose(*args):
    return c(*reversed(args))
