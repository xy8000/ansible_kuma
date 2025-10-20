ansible_role_install_docker_compose_container_from_git
=========

This role can be used to install a docker-compose configuration from a given git-repository.

Requirements
------------

None.

Role Variables
--------------

| Variable                         | Type              | Default              | Description                                             |
|----------------------------------|-------------------|----------------------|---------------------------------------------------------|
| git_repo_clone_url | string           | `<<OVERRIDE_ME>>`              | Repo to clone from        |
| git_repo_local_dest               | string           | `<<OVERRIDE_ME>>`              | Directory on the target machine to clone into from |
| expected_running_container_names  | string            | `<<OVERRIDE_ME>>` | List of expected container names to run after the docker-compose configuration has been applied  |
| docker_compose_file_name  | string            | `docker-compose.yaml` | File-Name of the docker-file tha t should be used by the role. |


Dependencies
------------

None.

Example Playbook
----------------

```yaml
  - role: ansible_role_install_docker_compose_container_from_git
    become: yes
    git_repo_clone_url: "git@github.com:xy8000/server_kuma"
    git_repo_local_dest: "~/git/server_kuma"
    docker_compose_file_name: "docker-compose.yml"
    expected_running_container_names:
      - "{{ upptime-kuma }}"
```

License
-------

BSD