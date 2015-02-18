#!/usr/bin/python3

import re

TASK_RE = re.compile('^[1-9][0-9]*:')

TASK_DELIMITER = ':'
HOUR_INTERVAL_SEPARATOR = " -> "
WORK_MESSAGE_SEPARATOR = " - "

DAY_LINE_FORMAT = "{:%A, %d %B %Y}"
DATE_PARSE_FORMAT = "%Y-%m-%d"

TRACKER_TASK_URL = "http://juno.codicefactory.com/tts/visualize.php?iddefect={}"

TASK_LINE_FORMAT = "* {} > [__{}__](" + TRACKER_TASK_URL + ") _({:%H:%M} - {:%H:%M})_"
NON_TASK_LINE_FORMAT = "* {} > __{}__ _({:%H:%M} - {:%H:%M})_"
