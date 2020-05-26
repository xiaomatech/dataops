#!/usr/bin/env python

import glob
import os


def get_das_home():
    das_home_dir = Script.get_stack_root() + "/data_analytics_studio"
    return das_home_dir


def get_das_lib(lib_glob):
    return glob.glob(os.path.join(get_das_home(), "lib", lib_glob))[0]
