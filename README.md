# Edge Application

This repo contains:
- application code and container image build instructions
- tekton pipelines to build/deploy this application
- ansible playbook & role to deploy

## Setup

Prerequisites:
- OCP cluster (tested on 4.9) with tekton and persistent storage
- Ansible Controller (tested on 4.1.1)

Setup Steps:
- Create application namespace
  - `oc new-project ed-app`
- Deploy secrets
  - [Create oauth token](https://docs.ansible.com/automation-controller/4.1.0/html/userguide/applications_auth.html#ug-tokens-auth-create) from the Ansible Controller
  - Create secrets from template `secrets/tower-auth.template.yml` -> `secrets/tower-auth.yml`
  - `oc apply -f secrets/tower-auth.yml`
- Import container images
  - `oc import-image registry.redhat.io/ansible-automation-platform-21/ee-supported-rhel8:latest --confirm`
  - `oc import-image registry.access.redhat.com/ubi8/ubi-minimal:8.5 --confirm`
- Deploy Tekton objects
  - `oc apply -f tekton/tower-job/`
- Trigger the pipeline from OpenShift Console (must use persistent storage RWO)

## Components

### Tekton 

- Fetch and build container
- Promote container to registry
- Trigger job on Ansible Controller deploy application to destination hosts
  - Example [Calling and watching AnsibleJob](https://gitlab.com/redhat-cop/ansible-ssa/role-aap-operator/-/blob/main/tasks/aap-controller-job.yml)
  - Probably just use controller collection and ee in Tekton to trigger job and wait for completion


### Ansible

#### Test Ansible execution locally

Take env vars from **secrets** directory.

```bash
podman run -it -e CONTROLLER_HOST=https://ansible-tower-host-url -e CONTROLLER_OAUTH_TOKEN=ansible-tower-api-token registry.redhat.io/ansible-automation-platform-21/ee-supported-rhel8:latest bash

# Run tests from inside the container, e.g. start playbook:
ansible-runner run /runner -p deploy-app.yml
```
