from pathlib import Path
from dataclasses import dataclass
import datetime

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


@dataclass
class Record:
    pub_date: str
    video_transcript: str
    video_summary: str
    minutes: str
    minutes_summary: str


def dir_name_to_time(dir_name: str):
    parts = dir_name.split("_")

    # Extract each part based on the expected position
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    hour = int(parts[3])
    minute = int(parts[4])
    second = int(parts[5])

    # Return the extracted fields
    return datetime.datetime(year, month, day, hour, minute, second)


if __name__ == "__main__":

    records = []

    for e in Path("html").glob("*"):
        if e.is_dir():
            when = dir_name_to_time(e.name)
            print(when)

            video_transcript = e / "video_transcript"
            if video_transcript.is_dir():
                video_transcript = video_transcript.relative_to("html")
            else:
                video_transcript = None

            video_summary = e / "video_summary.txt"
            if video_summary.is_file():
                video_summary = video_summary.relative_to("html")
            else:
                video_summary = None

            minutes_summary = e / "minutes_summary.txt"
            if minutes_summary.is_file():
                minutes_summary = minutes_summary.relative_to("html")
            else:
                minutes_summary = None

            minutes = e / "minutes.pdf"
            if minutes.is_file():
                minutes = minutes.relative_to("html")
            else:
                minutes = None

            records += [
                Record(
                    pub_date=when,
                    video_transcript=video_transcript,
                    video_summary=video_summary,
                    minutes=minutes,
                    minutes_summary=minutes_summary,
                )
            ]

    records = sorted(records, reverse=True, key=lambda r: r.pub_date)
    print(records)

    template = env.get_template("index.html")

    html = template.render(records=records)
    print(html)
    with open("html/index.html", "w") as f:
        f.write(html)
