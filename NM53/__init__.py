#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# NM53                                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program creates and updates backups of GitHub repositories of a user.   #
#                                                                              #
# copyright (C) 2017 Will Breaden Madden, wbm@protonmail.ch                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help                                        display help message
    --version                                         display version and exit
    --user=TEXT                                       GitHub username
    --parallel=BOOL                                   run git subprocesses in parallel       [default: false]
    --display_commands_only=BOOL                      display commands only, do not execute  [default: true]
    --update_only_currently_cloned_repositories=BOOL                                         [default: true]
    --number_of_pages=INT                             the number of pages to go through      [default: 5]
"""

name        = "NM53"
__version__ = "2019-11-26T1716Z"

import docopt
import json
import os
import subprocess
import sys
try:
    from urllib.request import urlopen
except:
    from urllib2 import urlopen

def main():
    options                                   = docopt.docopt(__doc__, version=__version__)
    user                                      = options["--user"]
    parallel                                  = options["--parallel"].lower() == "true"
    display_commands_only                     = options["--display_commands_only"].lower() == "true"
    update_only_currently_cloned_repositories = options["--update_only_currently_cloned_repositories"].lower() == "true"
    number_of_pages                           = int(options["--number_of_pages"])
    if user is None:
        print(__doc__)
        print("no user specified")
    for page_number in list(range(1, number_of_pages)):
        URL      = "https://api.github.com/users/{user}/repos?page={page_number}&per_page=1000".format(user=user, page_number=page_number)
        response = urlopen(URL)
        HTML     = response.read().decode("utf-8")
        JSON     = json.loads(HTML)
        command  = ""
        commands = ""
        for repository in JSON:
            print(repository['name'])
            if os.path.isdir(repository["name"]):
                print("repository {name} local copy found -- pull".format(name=repository["name"]))
                command = "cd {directory}; git pull; cd ..".format(directory=repository["name"])
            elif not update_only_currently_cloned_repositories:
                print("repository {name} local copy not found -- clone".format(name=repository["name"]))
                command = "git clone {URL}".format(URL = repository["clone_url"])
            if not display_commands_only:
                process = subprocess.Popen(
                    [command],
                    shell      = True,
                    executable = "/bin/bash",
                    stdout     = subprocess.PIPE
                )
                if not parallel:
                    process.wait()
            commands = commands + "\n" + command
        if display_commands_only:
            print(commands)
            print("\nNote: This program by default only lists commands, but can execute them. See --help for documentation on this.")

if __name__ == "__main__":
    main()
