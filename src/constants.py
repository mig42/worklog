#!/usr/bin/python3

import re

from enum import Enum

TASK_RE = re.compile('^[1-9][0-9]*:')

TASK_DELIMITER = ':'
HOUR_INTERVAL_SEPARATOR = " -> "
WORK_MESSAGE_SEPARATOR = " - "

DAY_LINE_FORMAT = "{:%A, %d %B %Y}"
DATE_PARSE_FORMAT = "%Y-%m-%d"

TRACKER_TASK_URL = "http://juno.codicefactory.com/tts/visualize.php?iddefect={taskid}"
APPLY_WORK_URL = "http://juno.codicefactory.com/tts/applyworkpost.php"

TASK_LINE_FORMAT = "* {elapsed} > __{worktype-human}[{message}](" + TRACKER_TASK_URL + ")__ _({start:%H:%M} - {end:%H:%M})_\n\
    * <form method=\"POST\" action=\"" + APPLY_WORK_URL + "\">\
<input type=\"hidden\" name=\"iddefect\" value=\"{taskid}\" />\
<input type=\"hidden\" name=\"fWorkType\" value=\"{worktype}\"/>\
<input type=\"hidden\" name=\"fWorkedMinutes\" value=\"{elapsed}\"/>\
<input type=\"hidden\" name=\"fTimestamp\" value=\"{date}\"/>\
<span class=\"input-text\" ><input type=\"text\" name=\"fRemainingHours\" size=\"5\"\
  maxlength=\"5\" value=\"{remaining}\"/></span> __hours remaining__\
<span class=\"input-submit\" ><input class=\"input-submit\"\
  type=\"submit\" value=\"↪\"/></span></form>"
NON_TASK_LINE_FORMAT = "* {elapsed} > __{message}__ _({start:%H:%M} - {end:%H:%M})_"

DEVELOP = ""
REVIEW = "Review "
VALIDATE = "Validate "

DEVELOP_CODE = "dev"
REVIEW_CODE = "rev"
VALIDATE_CODE = "val"

REMAINING_HOURS_TITLE = "Estimated remaining hours"

class WorkType(Enum):
    developer = 1
    reviewer = 2
    validator = 3
