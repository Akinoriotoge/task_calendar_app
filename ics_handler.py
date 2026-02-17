from datetime import datetime
import uuid


def generate_ics(task_row):
    """
    task_row = (id, title, description, start_datetime, end_datetime)
    """

    task_id = task_row[0]
    title = task_row[1]
    description = task_row[2]
    start_str = task_row[3]
    end_str = task_row[4]

    # 文字列 → datetime変換
    start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M")

    uid = f"{task_id}-{uuid.uuid4()}"
    now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    dtstart = start_dt.strftime("%Y%m%dT%H%M%S")
    dtend = end_dt.strftime("%Y%m%dT%H%M%S")

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//TaskCalendarApp//JP
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{now}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{title}
DESCRIPTION:{description}
BEGIN:VALARM
TRIGGER:-PT10M
ACTION:DISPLAY
DESCRIPTION:Reminder
END:VALARM
END:VEVENT
END:VCALENDAR
"""

    return ics_content

def save_ics(task_row, file_path):
    ics_data = generate_ics(task_row)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ics_data)
