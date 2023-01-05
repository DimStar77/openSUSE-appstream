#!/usr/bin/python3

# Copyright (c) 2014-2018 Dominique Leuenberger, Muhen, Switzerland
# Copyright (c) 2016 Raymond Wooninck, Vienna, Austria

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import subprocess
import sys
import glob

# Cleanup existing appdata found on the system

for oldappdata in glob.glob('/var/cache/app-info/xmls/*.xml.gz'):
  appdata=os.path.basename(oldappdata).strip('.xml.gz')
  subprocess.run(["/usr/bin/appstream-util", "uninstall", appdata])

# Install new appdata files - libzypp calls us with 6 parameters per repo:
# -R REPO_ALIAS -t REPO_TYPE -p REPO_METADATA_PATH [-R NEXT_REPO....]
# We can just blindly pass the parameters through to to helper
args=sys.argv[1:]

try:
  while args[0] == "-R":
    subprocess.run(["/usr/lib/AsHelper", "install", args[0], args[1], args[2], args[3], args[4], args[5]])
    args=args[6:]
except IndexError:
    pass

# Fixup icon that might have uncompressed with odd permissions
for icondir in glob.glob('/var/cache/app-info/icons/*'):
  os.chmod(icondir, 0o755)
