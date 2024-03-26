# -*- coding: utf-8 -*-
# v240326
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
_workplace_folder_path = current_directory

while(os.path.basename(_workplace_folder_path) != '_workplace'):
    print(os.path.basename(_workplace_folder_path))
    _workplace_folder_path = os.path.dirname(_workplace_folder_path)

source_folder_path = os.path.dirname(_workplace_folder_path)
config_file_path = os.path.join(_workplace_folder_path, 'naverBandAPI','config.yaml')