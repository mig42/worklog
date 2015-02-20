SET worklog_path=%~dp0
SET worklog_path=%worklog_path:~0,-1%

FOR /R "%worklog_path%\data" %%F IN (*.md) DO (
    SET html=%%F:~0,-2%html
    python3 "%worklog_path%\src\input.py" "%%F" | pandoc -s -f markdown -t html -c /css/github-markdown.css --template="%worklog_path%\templates\markdown.tpl" -o "%html%"
)
