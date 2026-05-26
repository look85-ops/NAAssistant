import urllib.request
import re
import sys
from datetime import datetime, timezone, timedelta

ICAL_URL = "https://calendar.google.com/calendar/ical/d7ece6d4f0c581734992579f18075782d50259311ec82f3b5c97226d0276fd6a%40group.calendar.google.com/public/basic.ics"
CALENDAR_NAME = "Наташа"

def parse_ical(text):
    events = []
    current = {}
    key_map = {
        "SUMMARY": "summary",
        "DESCRIPTION": "description",
        "LOCATION": "location",
    }
    for line in text.splitlines():
        line = line.strip()
        if line == "BEGIN:VEVENT":
            current = {}
        elif line == "END:VEVENT":
            if current.get("summary"):
                events.append(current)
            current = {}
        elif ":" in line:
            key, _, value = line.partition(":")
            if key in key_map:
                current[key_map[key]] = value
            elif key in ("DTSTART", "DTEND"):
                if value.endswith("Z"):
                    try:
                        dt = datetime.strptime(value[:-1], "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
                    except ValueError:
                        try:
                            dt = datetime.strptime(value[:-1], "%Y%m%d").replace(tzinfo=timezone.utc)
                        except ValueError:
                            continue
                    current["dtstart" if key == "DTSTART" else "dtend"] = dt
    return events

def main():
    try:
        resp = urllib.request.urlopen(ICAL_URL, timeout=10)
        text = resp.read().decode("utf-8")
    except Exception as e:
        print(f"[calendar] fetch failed: {e}")
        sys.exit(1)

    events = parse_ical(text)
    events.sort(key=lambda e: e.get("dtstart") or datetime.max.replace(tzinfo=timezone.utc))

    now = datetime.now(timezone.utc)
    week = now + timedelta(days=7)

    print(f"[{CALENDAR_NAME}] upcoming events (next 7 days):")
    print()

    found = 0
    for e in events:
        ds = e.get("dtstart")
        if ds and now <= ds <= week:
            found += 1
            day = ds.strftime("%a %d %b")
            time = ds.strftime("%H:%M") if ds.hour or ds.minute else "all-day"
            title = e.get("summary", "(no title)")
            print(f"  {day}  {time}  {title}")

    if not found:
        print("  (no events in the next 7 days)")

    print()

if __name__ == "__main__":
    main()
