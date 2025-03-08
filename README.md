# ansible-uptime-kuma

This collection contains modules that allow to configure [Uptime Kuma](https://github.com/louislam/uptime-kuma) with Ansible.

Python version 3.7+ and Ansible version 2.9+ are required.

Supported Uptime Kuma versions:

| Uptime Kuma     | ansible-uptime-kuma | ansible_kuma   |
| --------------- | ------------------- | -------------- |
| 1.21.3 - 1.23.2 | 1.0.0 - 1.2.0       | 1.0.0+         |
| 1.17.0 - 1.21.2 | 0.1.0 - 0.14.0      | 0.1.0 - 0.13.0 |

## Installation

This collection requires the python module [ansible_kuma](https://github.com/xy8000/ansible_kuma) to communicate with Uptime Kuma. It can be installed using pip:

```shell
pip install ansible_kuma
```

Alternately, you can install a specific version (e.g. `0.13.0`):

```shell
pip install ansible_kuma ==0.13.0
```

Then install the ansible collection itself:

```shell
ansible-galaxy collection install xy8000.uptime_kuma
```

Alternately, you can install a specific version (e.g. `0.14.0`):

```shell
ansible-galaxy collection install xy8000.uptime_kuma:==0.14.0
```

## Modules

The following modules are available:

- [api_key](https://github.com/xy8000/ansible-uptime-kuma/wiki/api_key)
- [api_key_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/api_key_info)
- [docker_host](https://github.com/xy8000/ansible-uptime-kuma/wiki/docker_host)
- [docker_host_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/docker_host_info)
- [game_list_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/game_list_info)
- [login](https://github.com/xy8000/ansible-uptime-kuma/wiki/login)
- [maintenance](https://github.com/xy8000/ansible-uptime-kuma/wiki/maintenance)
- [maintenance_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/maintenance_info)
- [monitor](https://github.com/xy8000/ansible-uptime-kuma/wiki/monitor)
- [monitor_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/monitor_info)
- [monitor_tag](https://github.com/xy8000/ansible-uptime-kuma/wiki/monitor_tag)
- [notification](https://github.com/xy8000/ansible-uptime-kuma/wiki/notification)
- [notification_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/notification_info)
- [proxy](https://github.com/xy8000/ansible-uptime-kuma/wiki/proxy)
- [proxy_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/proxy_info)
- [settings](https://github.com/xy8000/ansible-uptime-kuma/wiki/settings)
- [settings_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/settings_info)
- [setup](https://github.com/xy8000/ansible-uptime-kuma/wiki/setup)
- [status_page](https://github.com/xy8000/ansible-uptime-kuma/wiki/status_page)
- [status_page_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/status_page_info)
- [tag](https://github.com/xy8000/ansible-uptime-kuma/wiki/tag)
- [tag_info](https://github.com/xy8000/ansible-uptime-kuma/wiki/tag_info)

## Getting started

Directly after the installation of Uptime Kuma, the initial username and password must be set:

```yaml
- name: Specify the initial username and password
  xy8000.uptime_kuma.setup:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
```

For future requests you can either use these credentials directly or a token that must be generated once.
The token usage is recommended because frequent logins lead to a rate limit. In this example we create a new monitor.

Option 1 (not recommended): Create a monitor by using the credentials directly:

```yaml
- name: Login with credentials and create a monitor
  xy8000.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
    name: Google
    type: http
    url: https://google.com
    state: present
```

Option 2 (recommended): Generate a token and create a monitor by using this token:

```yaml
- name: Login with credentials once and register the result
  xy8000.uptime_kuma.login:
    api_url: http://127.0.0.1:3001
    api_username: admin
    api_password: secret123
  register: result

- name: Extract the token from the result and set it as fact
  set_fact:
    api_token: "{{ result.token }}"

- name: Login by token and create a monitor
  xy8000.uptime_kuma.monitor:
    api_url: http://127.0.0.1:3001
    api_token: "{{ api_token }}"
    name: Google
    type: http
    url: https://google.com
    state: present
```
