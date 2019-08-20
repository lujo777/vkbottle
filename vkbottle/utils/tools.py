
"""
VKBOTTLE WORK TOOLS
"""

from copy import deepcopy


def dict_of_dicts_merge(x, y):
    z = {}
    try:
        overlapping_keys = x.keys() & y.keys()
        for key in overlapping_keys:
            z[key] = dict_of_dicts_merge(x[key], y[key])
        for key in x.keys() - overlapping_keys:
            z[key] = deepcopy(x[key])
        for key in y.keys() - overlapping_keys:
            z[key] = deepcopy(y[key])
    except AttributeError:
        pass
    return z


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
