from subprocess import call
import os
cwd = os.getcwd()
command = "sass --scss --debug-info --compass --watch %s/styleguide/static/scss/:%s/styleguide/static/.sass-cache/livereload/" % (cwd,cwd)
os.system(command)