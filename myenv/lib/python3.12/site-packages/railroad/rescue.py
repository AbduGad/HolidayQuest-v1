# -*- coding: utf-8 -*-


def reraise(e):
    raise e


def nop(*args, **kwargs):
    pass


def rescue(f, on_success, on_error=reraise, on_complete=nop):
    '''
    Functional try-except-finally

    :param function f: guarded function
    :param function on_succes: called when f is executed without error
    :param function on_error: called with `error` parameter when f failed
    :param function on_complete: called as finally block
    :returns function: call signature is equal f signature
    '''
    def _rescue(*args, **kwargs):
        try:
            return on_success(f(*args, **kwargs))
        except Exception as e:
            return on_error(e)
        finally:
            on_complete()

    return _rescue
