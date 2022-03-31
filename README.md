# Edge Application

This repo contains:
- application code and container image build instructions
- tekton pipelines to build/deploy this application
- ansible playbook & role to deploy


## Tekton 

- Fetch and build container
- Promote container to registry
- Trigger job on Ansible Controller deploy application to destination hosts
  - [Example pipeline](https://github.com/tektoncd/catalog/blob/main/task/ansible-tower-cli/0.1/ansible-tower-cli.yaml)
  - Example [Calling and watching AnsibleJob](https://gitlab.com/redhat-cop/ansible-ssa/role-aap-operator/-/blob/main/tasks/aap-controller-job.yml)
  - Probably just use controller collection and ee in Tekton to trigger job and wait for completion