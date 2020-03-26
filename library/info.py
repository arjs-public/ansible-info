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
    step: "Step something"
    msg: "We do something"
    file: file
"""

RETURN = '''
path:
  description: Setup the info json
  returned: success
  type: string
  sample: "/tmp/info.json"
'''

import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from tempfile import mkstemp, mkdtemp

path = None

def main():
    global path
    module = AnsibleModule(
        argument_spec = dict(
            state     = dict(default='send', choices=['send', 'setup']),
            phase     = dict(default=None),
            step      = dict(default=None),
            msg       = dict(default='?'),
            prefix    = dict(default='info'),
            suffix    = dict(default='.json'),
            path      = dict(default='/tmp'),
            file      = dict(default='/tmp/info.json')
        )
    )

    try:
        _prefix = "info" if not "prefix" in module.params else module.params['prefix']
        _suffix = ".json" if not "suffix" in module.params else module.params['suffix']
        _path = "/tmp" if not "path"in module.params else module.params['path']
        _file = "/tmp/info.json" if not "file"in module.params else module.params['file']
        _state = '' if not 'state' in module.params else module.params['state']
        if _state == 'setup':
            global path
            handle, _file = mkstemp(
               prefix=_prefix,
               suffix=_suffix,
               dir=_path
            )
            if not os.path.exists(_file):
              raise RuntimeError('No file %s found' % _file)

        elif _state == 'send':
            step = 'default' if not 'step' in module.params else module.params['step']
            msg = 'leer' if not 'msg' in module.params else module.params['msg']
            if not _file: 
              _file = mkstemp(
                  prefix=_prefix,
                  suffix=_suffix,
                  dir=_path
              )
              #path = os.path.join(path, "info.json") 
          
            if not os.path.exists(_file):
              raise RuntimeError('No file %s found' % _file)

            with open(_file, "w") as file_pointer:
              file_pointer.write(step.strip() + '\n')
              file_pointer.write(msg.strip() + '\n')

        else:
          path = ''

        module.exit_json(changed=True, path=_file)

    except Exception:
        e = get_exception()
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
