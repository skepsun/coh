import absl.flags
import absl.logging

from ml_collections import ConfigDict
from ml_collections.config_flags import config_flags


def define_flags_with_default(**kwargs):
    for key, val in kwargs.items():
        if isinstance(val, tuple):
            val, help_str = val
        else:
            help_str = ""

        if isinstance(val, ConfigDict):
            config_flags.DEFINE_config_dict(key, val)
        elif isinstance(val, bool):
            # Note that True and False are instances of int.
            absl.flags.DEFINE_bool(key, val, help_str)
        elif isinstance(val, int):
            absl.flags.DEFINE_integer(key, val, help_str)
        elif isinstance(val, float):
            absl.flags.DEFINE_float(key, val, help_str)
        elif isinstance(val, str):
            absl.flags.DEFINE_string(key, val, help_str)
        else:
            raise ValueError("Incorrect value type")
    return absl.flags.FLAGS, kwargs


