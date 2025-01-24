# -*- coding: utf-8 -*-

from functools import wraps, partial
from six.moves import reduce
from toolz import concatv, cons, remove


def actions(acts, done):
    '''
    Prepare actions pipeline.

    :param tuple acts: called functions
    :param function done: get result from actions
    :returns function: function that starts executio
    '''

    def _intermediate(acc, action):
        result = action(acc['state'])
        values = concatv(acc['values'], [result['answer']])

        return {'values': values, 'state': result['state']}

    def _actions(seed):
        init = {'values': [], 'state': seed}

        result = reduce(_intermediate, acts, init)

        keep = remove(lambda x: x is None, result['values'])

        return done(keep, result['state'])

    return _actions


def lift(fn=None, state_fn=None):
    """
    The lift decorator function will be used to abstract away the management
    of the state object used as the intermediate representation of actions.

    :param function answer: a function to provide
                            the result of some action given a value
    :param function state: a function to provide what the new state looks like
    :returns function: a function suitable for use in actions
    """
    if fn is None:
        return partial(lift, state_fn=state_fn)

    @wraps(fn)
    def _lift(*args, **kwargs):
        def _run(state):
            ans = fn(*cons(state, args), **kwargs)
            s = state_fn(state) if state_fn is not None else ans

            return {'answer': ans, 'state': s}
        return _run
    return _lift


def result(values, state):
    '''
    Return computed value from actions
    '''
    return state
