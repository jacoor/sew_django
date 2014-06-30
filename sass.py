#!/usr/bin/env python
import os
cwd = os.getcwd()
command = "sass --scss --debug-info --sourcemap --compass --watch --poll %s/sew_django/static/scss/:%s/sew_django/static/.sass-cache" % (cwd,cwd)
os.system(command)