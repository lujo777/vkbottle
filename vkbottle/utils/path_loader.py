import importlib.util

import os

from .plugin import Plugin

from ..utils import Logger

import re

import time


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_plugins_by_file(path, logger: Logger):
    module = import_module(path, path)
    plugins = []

    if hasattr(module, "plugin") and isinstance(module.plugin, Plugin):
        plugins.append(module.plugin)

    if hasattr(module, "plugins") and isinstance(module.plugins, (list, tuple)):
        plugins.extend(module.plugins)

    return plugins


def load_plugins(folder, logger: Logger):
    plugins_list = []
    path = 'plugins/'

    if len(os.listdir(folder)) > 0:

        # [Feature] Progress Bar
        logger.progress_bar(0, len(os.listdir(folder)), prefix='Downloading your plugins from "{}/":'.format(folder),
                           suffix='Complete', length=50)

        for i, name in enumerate(os.listdir(folder)):
            path = os.path.join(folder, name)

            if os.path.isdir(path):
                plugins_list += load_plugins(path, logger)

            elif re.match(r"^[^_].*\.py$", name):
                plugins_list += load_plugins_by_file(path, logger)

            # Progress Bar Update Delay
            time.sleep(0.05)

            # Update Progress Bar
            logger.progress_bar(i + 1, len(os.listdir(folder)), prefix='Downloading your plugins from "{}/":'.format(folder),
                               suffix='Complete', length=50)

    logger('Found {} Plugins in \x1b[93;1m{}\x1b[0m{}'.format(
        len(plugins_list),
        os.path.dirname(path),
        ':' if len(plugins_list) > 0 else ''),
        *[plugin.name + (' \x1b[37m(' + str(plugin.description) + ')\x1b[0m' if plugin.description is not None else '') for plugin in plugins_list], separator='\n \u25CF ',
    )

    return plugins_list
