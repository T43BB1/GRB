https://youtu.be/cnmoZ05Sbfc

# GRB

## Overview

GRB is an automation and management framework designed to streamline infrastructure operations and testing across various environments such as Ansible, Docker, Nginx, Node.js, and Oracle. This repository provides scripts, configuration files, and utilities for orchestrating deployment, configuration, and validation tasks in a unified and programmable way.

## Main Components

- **main.py**  
  The primary entry point for running automation and testing workflows.

- **main_onestop.py / main_onebyone_test.py**  
  - `main_onestop.py`: Runs the whole process in a single workflow (one-stop execution).
  - `main_onebyone_test.py`: Allows for step-by-step or individual test execution.

- **ansible.cfg / ansible_filter_plugins/**  
  Ansible configuration file and custom filter plugins to extend playbook capabilities.

- **docker/**  
  Contains Docker-related resources and scripts for environment setup and management.

- **linux/**  
  Linux-specific scripts and resources for configuring and managing Linux environments.

- **nginx/**  
  Nginx configuration files and supporting resources.

- **nodejs/**  
  Utilities and files for managing Node.js-based services or testing environments.

- **oracle/**  
  Oracle database scripts, configuration, and resources.

- **tui/**  
  Terminal User Interface (TUI) components for interactive command-line operations.

- **log.json / log/**  
  Logging directory and files for capturing execution results and operational logs.

- **inventory**  
  Ansible inventory file specifying the target hosts and groups.

## Directory Structure

```
.
├── ansible.cfg
├── ansible_filter_plugins/
├── docker/
├── inventory
├── linux/
├── log/
├── log.json
├── main.py
├── main_onebyone_test.py
├── main_onestop.py
├── nginx/
├── nodejs/
├── oracle/
├── readme.md
└── tui/
```


