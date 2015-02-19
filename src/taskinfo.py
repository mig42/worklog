#!/usr/bin/python3

import base64
import constants
import os
import sys
import urllib.request

from html.parser import HTMLParser


def main():
    if len(sys.argv) < 2:
        print("Usage: {} <task_id>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    passwd_file_path = os.path.join(get_current_dir(), constants.PASSWORD_FILE_NAME)

    if not os.path.exists(passwd_file_path):
        print("Password file {} couldn't be found.".format(passwd_file_path), file=sys.stderr)
        sys.exit(1)

    authstring = parse_password_file(passwd_file_path)

    retriever = TaskDataRetriever(constants.TRACKER_TASK_URL, authstring)
    for task_id in sys.argv[1:]:
        print(retriever.get_remaining_task_time(task_id))

def get_current_dir():
    return os.path.dirname(os.path.abspath(__file__))

def parse_password_file(password_file_path):
    with open(password_file_path, 'r') as passwd_file:
        lines = [line.strip() for line in passwd_file]
    if len(lines) < 1:
        return ""
    return lines[0]

def test(task_id, authstring):
    retriever = TaskDataRetriever(constants.TRACKER_TASK_URL, authstring)
    print(retriever.get_remaining_task_time(task_id))


class TaskDataRetriever:

    def __init__(self, base_url, authstring):
        self._base_url = base_url
        self._authstring = authstring.strip()
        self._value_cache = {}

    def get_remaining_task_time(self, task_id):
        if task_id in self._value_cache.keys():
            return self._value_cache[task_id]

        parser = TaskPageParser()

        request = self.get_request(task_id)
        with urllib.request.urlopen(request) as http_conn:
            try:
                parser.feed(http_conn.read().decode("utf8"))
                self._value_cache[task_id] = parser.get_remaining_task_time()
                return self._value_cache[task_id]
            finally:
                parser.close()


    def get_request(self, task_id):
        request = urllib.request.Request(self._base_url.format(task_id))
        base64string = base64.b64encode(bytes(self._authstring, "utf8"))
        request.add_header("Authorization", b'Basic ' + base64string)
        return request

class TaskPageParser(HTMLParser):

    def __init__(self):
        super(TaskPageParser, self).__init__()
        self._remaining_task_time = 0
        self._previous_data = ""
        self._current_tag_class = None
        self._is_finished = False

    def handle_starttag(self, tag, attrs):
        self._current_tag_class = (tag, self.get_tag_class(attrs))

    def get_tag_class(self, attrs):
        for attr in attrs:
            if attr[0] == "class":
                return attr[1]
        return ""

    def handle_data(self, data):
        if self._is_finished:
            return

        if self._previous_data == constants.REMAINING_HOURS_TITLE:
            if self._current_tag_class == ("td", "tableFieldContent"):
                self._remaining_task_time = float(data.strip())
                self._is_finished = True
            return
        self._previous_data = data.strip()

    def get_remaining_task_time(self):
        if self._remaining_task_time < 0:
            return 0
        return self._remaining_task_time


if __name__ == "__main__":
    main()
