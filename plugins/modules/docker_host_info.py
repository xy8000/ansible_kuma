#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Lucas Held <lucasheld@hotmail.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r'''
---
extends_documentation_fragment:
  - xy8000.uptime_kuma.uptime_kuma

module: docker_host_info
author: Lucas Held (@lucasheld)
short_description: Retrieves facts about docker hosts.
description: Retrieves facts about docker hosts.

options:
  id:
    description:
      - The id of the docker host to inspect.
      - Only required if no I(name) specified.
    type: int
  name:
    description:
      - The name of the docker host to inspect.
      - Only required if no I(id) specified.
    type: str
'''

EXAMPLES = r'''
- name: get all docker hosts
  xy8000.uptime_kuma.docker_host_info:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result
'''

RETURN = r'''
docker_hosts:
  description: The docker hosts as list
  returned: always
  type: complex
  contains:
    id:
      description: The id of the docker host.
      returned: always
      type: int
      sample: 1
    userID:
      description: The user id of the docker host.
      returned: always
      type: int
      sample: 1
    dockerType:
      description: The docker type of the docker host.
      returned: always
      type: str
      sample: socket
    dockerDaemon:
      description: The docker daemon of the docker host.
      returned: always
      type: str
      sample: /var/run/docker.sock
    name:
      description: The name of the docker host.
      returned: always
      type: str
      sample: docker host 1
'''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.xy8000.uptime_kuma.plugins.module_utils.common import common_module_args, get_docker_host_by_name
from ansible.module_utils.basic import missing_required_lib

try:
    from uptime_kuma_api import UptimeKumaApi
    HAS_UPTIME_KUMA_API = True
except ImportError:
    HAS_UPTIME_KUMA_API = False


def run(api, params, result):
    if params["id"]:
        docker_host = api.get_docker_host(params["id"])
        result["docker_hosts"] = [docker_host]
    elif params["name"]:
        docker_host = get_docker_host_by_name(api, params["name"])
        result["docker_hosts"] = [docker_host]
    else:
        result["docker_hosts"] = api.get_docker_hosts()


def main():
    module_args = dict(
        id=dict(type="int"),
        name=dict(type="str"),
    )
    module_args.update(common_module_args)

    module = AnsibleModule(module_args, supports_check_mode=True)
    params = module.params

    if not HAS_UPTIME_KUMA_API:
        module.fail_json(msg=missing_required_lib("uptime_kuma_api"))

    api = UptimeKumaApi(params["api_url"], timeout=params["api_timeout"], headers=params["api_headers"], ssl_verify=params["api_ssl_verify"], wait_events=params["api_wait_events"])
    api_token = params.get("api_token")
    api_username = params.get("api_username")
    api_password = params.get("api_password")
    if api_token:
        api.login_by_token(api_token)
    elif api_username and api_password:
        api.login(api_username, api_password)
    else:
        # autoLogin for enabled disableAuth
        api.login()

    result = {
        "changed": False
    }

    try:
        run(api, params, result)

        api.disconnect()
        module.exit_json(**result)
    except Exception:
        api.disconnect()
        error = traceback.format_exc()
        module.fail_json(msg=error, **result)


if __name__ == '__main__':
    main()
