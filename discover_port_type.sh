#!/bin/bash

ansible-playbook -i inventory mac_add.yml
python discover_trunks.py ./mac_tables/dev_172.16.148.1.json
