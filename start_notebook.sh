#!/usr/bin/env bash
# Start JupyterLab on port 5000 for working with the fine-tuning notebooks.
# Switch back to the web app with:  bash start.sh

set -e
exec /home/runner/workspace/.pythonlibs/bin/jupyter lab \
  --config=/home/runner/workspace/jupyter_config.py \
  --no-browser
