# -*- coding: utf-8 -*-

import subprocess

# Command with shell expansion
subprocess.call('python3 start_server.py -p 7777 -a 127.0.0.1', shell=True)
