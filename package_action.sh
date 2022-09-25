#!/bin/bash
set -e

virtualenv -p `which python3.7` virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
zip -r notion_api.zip virtualenv notion config.yaml __main__.py
