import importlib
import inspect
import os

__version__ = '0.11.0'
__config_instance = None
SETTINGS_PATH_VAR = 'APP_SETTING_MODULE'
DEFAULT_ENV = 'local'
DEFAULT_SETTINGS_MODULE = 'settings'


def get(key=None, default=None):
    global __config_instance

    def resolve_config_path():
        # todo: future implementaion can do this as well
        # app_env = os.environ.get('APP_ENV') or DEFAULT_ENV
        base_path = os.environ.get(SETTINGS_PATH_VAR, None)
        if base_path is None:
            base_path = 'settings'

        return base_path

    # global config_instance
    if __config_instance is None:
        try:
            _settings_module = importlib.import_module(resolve_config_path())
            __config_instance = load_settings(_settings_module)
        except:
            __config_instance = {}

    return __config_instance.get(key, default)


def merge(settings, override=False):
    new_settings = load_settings(settings)
    global __config_instance

    if __config_instance is None:
        __config_instance = {}

    for key, value in new_settings.iteritems():
        if key not in __config_instance or override:
            __config_instance[key] = value


def load_settings(settings_module):
    if type(settings_module) is dict:
        return settings_module

    result = {}
    if inspect.ismodule(settings_module):
        for setting in (s for s in dir(settings_module) if not s.startswith('_')):
            setting_value = getattr(settings_module, setting)
            if not inspect.ismodule(setting_value):
                result[setting] = setting_value

    return result

def reset():
    if __config_instance is not None:
        __config_instance.clear()