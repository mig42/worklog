#!/usr/bin/python3
"""Simple worklog parser"""

import constants
import sys
import taskinfo

from constants import WorkType
from datetime import datetime, timedelta
from os import path

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

def timedelta_str(my_timedelta):
    if my_timedelta < timedelta(0):
        return "00:00"
    hours, minutes = divmod(my_timedelta.total_seconds(), 3600)
    minutes, seconds = divmod(minutes, 60)

    return "{:02}:{:02}".format(int(hours), int(minutes))

class WorklogParser:

    def __init__(self):
        self._current_day = datetime.today()
        self._task_parser = taskinfo.TaskDataRetriever(constants.TRACKER_TASK_URL)

    def parse_line(self, line):
        clean_line = line.strip()
        if clean_line.startswith("# "):
            return self.parse_title(clean_line)
        if clean_line.startswith("## "):
            return self.parse_month(clean_line)
        if self.is_verbatim_line(clean_line):
            return line
        if clean_line.startswith("### "):
            return "\n" + self.parse_day(clean_line)
        if clean_line.startswith("* "):
            return self.parse_work(clean_line)
        return None

    def is_verbatim_line(self, line):
        return line.startswith("% ")

    def parse_title(self, line):
        return self.get_title_line("#", line[2:5].lower(), line[2:])

    def parse_month(self, line):
        return self.get_title_line("##", line[3:6].lower(), line[3:])

    def get_title_line(self, title_mark, anchor_id, text):
        return "{0} <a id=\"{1}\" class=\"anchor\" href=\"#{1}\" aria-hidden=\"true\">\
<span class=\"octicon octicon-link\"></span></a>{2}".format(title_mark, anchor_id, text)

    def parse_day(self, day_line):
        date_text = day_line[4:14]
        self._current_day = datetime.strptime(date_text, constants.DATE_PARSE_FORMAT)
        text = constants.DAY_LINE_FORMAT.format(self._current_day)
        return self.get_title_line("###", date_text, text)

    def parse_work(self, work_line):
        start_time_text, end_time_text, message, work_type = self.split_work_line(work_line)

        start_time, end_time = self.get_times(start_time_text, end_time_text)
        elapsed_time = end_time - start_time

        values = {
            "elapsed": timedelta_str(elapsed_time),
            "start": start_time,
            "end": end_time,
            "message": message,
        }

        if not constants.TASK_RE.match(message):
            return constants.NON_TASK_LINE_FORMAT.format_map(values)

        task_id, task_name = message.split(":", 1)
        values["taskid"] = task_id
        values["message"] = task_name.strip()
        values["worktype-human"] = self.get_work_type_text(work_type)
        values["worktype"] = self.get_work_type_code(work_type)
        values["remaining"] = self._task_parser.get_remaining_task_time(task_id)
        values["date"] = "{:%Y-%m-%d}".format(self._current_day)

        return constants.TASK_LINE_FORMAT.format_map(values)

    def split_work_line(self, work_line):
        date_part, message = work_line[2:].strip().split(constants.WORK_MESSAGE_SEPARATOR, 1)
        start_time, end_time = date_part.split(constants.HOUR_INTERVAL_SEPARATOR, 1)
        message, work_type = self.parse_message(message.strip("*_ "))

        return (start_time, end_time, message, work_type)

    def get_times(self, start_time_text, end_time_text):
        start_time = self.build_date(start_time_text)
        end_time = self.build_date(end_time_text)

        if start_time > end_time:
            return start_time, start_time
        return start_time, end_time

    def parse_message(self, message):
        if message.endswith("[v]"):
            return message[:-3], WorkType.validator
        if message.endswith("[r]"):
            return message[:-3], WorkType.reviewer
        return message, WorkType.developer

    def build_date(self, time):
        try:
            date_string = "{:%Y-%m-%d} {}".format(self._current_day, time)
            return datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        except ValueError:
            return datetime.now()

    def get_work_type_text(self, work_type):
        if work_type == WorkType.reviewer:
            return constants.REVIEW
        if work_type == WorkType.validator:
            return constants.VALIDATE
        return constants.DEVELOP

    def get_work_type_code(self, work_type):
        if work_type == WorkType.reviewer:
            return constants.REVIEW_CODE
        if work_type == WorkType.validator:
            return constants.VALIDATE_CODE
        return constants.DEVELOP_CODE


if __name__ == "__main__":
    main()
