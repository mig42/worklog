#!/usr/bin/python3
"""Simple worklog parser"""

import constants
import re
import sys

from datetime import datetime, date
from os import path

TASK_RE = re.compile('^[1-9][0-9]*:')

TASK_LINE_FORMAT = \
    "* {{}} > [__{{}}__]({}) _({{:%H:%M}} - {{:%H:%M}})_".format(constants.TRACKER_TASK_URL)

NON_TASK_LINE_FORMAT = "* {} > __{}__ _({:%H:%M} - {:%H:%M})_"

def main():
    if len(sys.argv) < 2:
        print("Usage: {} <log_file>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    if not path.isfile(file_path):
        print("File not found: ", file_path, file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'r') as log_file:
        worklog_parser = WorklogParser()
        for file_line in log_file:
            parsed_line = worklog_parser.parse_line(file_line)
            if parsed_line is None:
                continue
            print(parsed_line)


def is_verbatim_line(line):
    return line.startswith("## ") or line.startswith("% ")

def split_work_line(work_line):
    date_part, message = work_line[2:].strip().split(" - ", 1)
    start_time, end_time = date_part.split(" -> ", 1)
    message = message.strip("*_")

    return (start_time, end_time, message)

def timedelta_str(timedelta):
    hours, minutes = divmod(timedelta.total_seconds(), 3600)
    minutes, seconds = divmod(minutes, 60)

    return "{:02}:{:02}".format(int(hours), int(minutes))

class WorklogParser:

    def __init__(self):
        self._current_day = datetime.today()

    def parse_line(self, line):
        clean_line = line.strip()
        if is_verbatim_line(clean_line):
            return line
        if clean_line.startswith("### "):
            return "\n" + self.parse_day(clean_line)
        if clean_line.startswith("* "):
            return self.parse_work(clean_line)
        return None

    def parse_day(self, day_line):
        self._current_day = datetime.strptime(day_line[4:14], "%Y-%m-%d")
        return "### {:%A, %d %B %Y}".format(self._current_day)

    def parse_work(self, work_line):
        start_time_text, end_time_text, message = split_work_line(work_line)
        start_time = self.build_date(start_time_text)
        end_time = self.build_date(end_time_text)
        elapsed_time = timedelta_str(end_time - start_time)

        if not TASK_RE.match(message):
            return NON_TASK_LINE_FORMAT.format(elapsed_time, message, start_time, end_time)

        task_id, task_name = message.split(":", 1)
        return TASK_LINE_FORMAT.format(
            elapsed_time, task_name.strip(), task_id, start_time, end_time)

    def build_date(self, time):
        try:
            date_string = "{:%Y-%m-%d} {}".format(self._current_day, time)
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.now()


if __name__ == "__main__":
    main()
