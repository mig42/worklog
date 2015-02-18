#!/usr/bin/python3

import re

from enum import Enum

TASK_RE = re.compile('^[1-9][0-9]*:')

TASK_DELIMITER = ':'
HOUR_INTERVAL_SEPARATOR = " -> "
WORK_MESSAGE_SEPARATOR = " - "

DAY_LINE_FORMAT = "{:%A, %d %B %Y}"
DATE_PARSE_FORMAT = "%Y-%m-%d"

TRACKER_TASK_URL = "http://juno.codicefactory.com/tts/visualize.php?iddefect={}"

TASK_LINE_FORMAT = "* {} > __{}[{}](" + TRACKER_TASK_URL + ")__ _({:%H:%M} - {:%H:%M})_"
NON_TASK_LINE_FORMAT = "* {} > __{}__ _({:%H:%M} - {:%H:%M})_"

DEVELOP = ""
REVIEW = "Review "
VALIDATE = "Validate "

PASSWORD_FILE_NAME = "passwd"

class WorkType(Enum):
    developer = 1
    reviewer = 2
    validator = 3
