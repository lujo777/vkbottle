from collections import MutableMapping


def dict_of_dicts_merge(d1, d2):
    '''
    Update two dicts of dicts recursively,
    if either mapping has leaves that are non-dicts,
    the second's leaf overwrites the first's.
    '''
    for k, v in d1.items(): # in Python 2, use .iteritems()!
        if k in d2:
            # this next check is the only difference!
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = dict_of_dicts_merge(v, d2[k])
            # we could further check types and merge as appropriate here.
    d3 = d1.copy()
    d3.update(d2)
    return d3


def make_priority_path(first: dict, plugin_priority, priority, compile, second):
    if plugin_priority not in first:
        first[plugin_priority] = {}
    if priority not in first[plugin_priority]:
        first[plugin_priority][priority] = {}
    if compile is not None:
        first[plugin_priority][priority][compile] = second
    else:
        first[plugin_priority][priority] = second
    return first
