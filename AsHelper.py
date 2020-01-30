#!/usr/bin/python3

# Copyright (c) 2018 Dominique Leuenberger, Muhen, Switzerland

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
import sys
import cmdln
import createrepo_c as cr

RPMMD="repodata"
YAST2="suse/setup/descr"
CMD="appstream-util install-origin \"{NAME}\" \"{APPDATA}\" \"{ICONS}\""

class AsInstall(cmdln.Cmdln):
  """
    ${name}
            Helper to collect information about AppStream Metadata and install
            them into the system cache. This helper is intended to be called by libzypp

    ${option_list}

    Currently there is only one command available: install
  """

  @cmdln.option("-R", dest="alias", help="The alias of the repository")
  @cmdln.option("-t", dest="type", help="Repsitory type (rpm-md, yast2)")
  @cmdln.option("-p", dest="path", help="base directory for this repositories cache")
  def do_install(self, subcmd, opts):
      """
      ${cmd_name}: Helper to collect information about AppStream Metadata and install
               them into the system cache. This helper is intended to be called by libzypp
      ${cmd_usage}
      ${cmd_option_list}
      """
      RET={}
      if opts.type == "yast2":
          ### yast2 type is 'easy': the files are called appstream.xml.gz and appstream-icons.tar.gz
          ROOT=os.path.join(opts.path, YAST2)
          RET = {'appdata': os.path.join(ROOT,'appstream.xml.gz'), 'appdata-icons': os.path.join(ROOT,'appstream-icons.tar.gz')}
          pass
      elif opts.type == "rpm-md":
          RET=self.parse_rpmmd(opts.path)
          pass
      else:
          print("Repotype %s unknown" % opts.type)

      if RET:
          os.system(CMD.format(NAME=opts.alias.replace(':','_'), APPDATA=RET['appdata'], ICONS=RET['appdata-icons']))
      else:
          print("could not find appdata tarball and/or icons")

  def parse_rpmmd(self, repopath):
    repomd = cr.Repomd(os.path.join(repopath ,RPMMD, 'repomd.xml'))
    RET={}
    for datatype in ['primary', 'appdata', 'appdata-icons']:
        try:
            RET[datatype] = os.path.join(repopath, repomd[datatype].location_href)
        except KeyError:
            RET={}
            break
    return RET


if __name__ == "__main__":
    asinst = AsInstall()
    sys.exit( asinst.main() )
    
