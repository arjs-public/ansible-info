#!/usr/bin/python
#coding: utf-8 -*-

# (c) 2016 Krzysztof Magosa <krzysztof@magosa.pl>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: info
version_added: "2.3"
author:
  - Alex Schiessl
short_description: Info...
description:
  - Info..
options:
  state:
    description:
      - Whether to setup, send
    required: true
    choices: [ "setup", "send" ]
    default: send
  phase:
    description:
      - Phase to use
    required: false
    default: null
  step:
    description:
      - Step to use
    required: false
    default: null
  msg:
    description:
      - Info to use
    required: false
    default: ""
'''

EXAMPLES = """
- name: Report the progress
  info:
    state: setup
    phase: deploy
    step: "Do something"
    msg: "We do something"

- name: create temporary file
  info:
    state: setup
    phase: deploy
    step: "Do something"
    msg: file
"""

RETURN = '''
path:
  description: Setup the info json
  returned: success
  type: string
  sample: "/tmp/info.json"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from tempfile import mkstemp, mkdtemp
import os

def main():
    module = AnsibleModule(
        argument_spec = dict(
            state     = dict(default='send', choices=['send', 'setup']),
            phase     = dict(default=None),
            step      = dict(default=None),
            msg       = dict(default='')
        )
    )

    try:
        if module.params['state'] == 'setup':
            path='.'
#            handle, path = mkstemp(
#                prefix=module.params['prefix'],
#                suffix=module.params['suffix'],
#                dir=module.params['path']
#            )
#            close(handle)
            print "SETUP"
        elif module.params['state'] == 'send':
            path = mkdtemp(
                prefix="tmp",
                suffix=".json",
                dir="/tmp"
            )
            msg = module.params['msg'] if module.params['msg'] else 'leer'
            with open(os.path.join(path, "info.json"), "w") as file_pointer:
              file_pointer.write(msg)

        module.exit_json(changed=True, path=path)
    except Exception:
        e = get_exception()
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
