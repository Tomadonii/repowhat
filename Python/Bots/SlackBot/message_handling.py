
import datetime
import locale
import os
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from slack_sdk import WebClient
from slack_bolt import App
import re

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"], "/slack/events")


app = App(
    token=os.environ["SLACK_TOKEN"],
    signing_secret=os.environ["SIGNING_SECRET"]
    )


client = WebClient(token=os.environ["SLACK_TOKEN"])
BOT_ID = client.api_call("auth.test")["user_id"]

Weekdays = [["montag", "monday", "mo", "mon"],["dienstag", "tuesday", "di", "tu", "die", "tue"],["mittwoch", "wednesday", "mi", "we", "wed"],["thursday", "donnerstag","th","do", "thu"],["friday", "freitag","fr", "fri"]]


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    event_user_id = event.get("user")
    messages = fetch_history_messages(event)
    if event_user_id == BOT_ID:
        return
    date = handle_text_specs(event)
    for message in messages:
        history_timestamp, history_text,  history_user = handle_message(message)
        print(history_timestamp)
        if history_user != event_user_id: 
            return    

def handle_text_specs(event):
    event_message_text = event.get("text").lower()
    event_message_text = str(event_message_text)

    # Filter through the text with these patterns one by one
    # Jahr pattern > KW Pattern > Weekday Pattern (Seperator always in between these patterns)
    pattern_jahr = re.compile("^(\d{2,4})\-(.*)")
    pattern_kw = re.compile("^(\d{1,2})(.*)")
    pattern_weekday = re.compile("^([a-zA-Z]{2,10})\:(.*)")
    pattern_seperator = re.compile("^[^A-Za-z0-9](.*)")

    lines = iterate_message_lines(event_message_text)
    jahr, kw, weekday = epoch_to_dates.event_ts_date(event)

    for line in lines:

        result_line_jahr = pattern_jahr.match(line)
        if result_line_jahr is not None:
            jahr = result_line_jahr.group(1)
            line = result_line_jahr.group(2)
            result_line_seperator = pattern_seperator.match(line)
            if result_line_seperator is not None:
                line = result_line_seperator.group(1)
            if len(jahr) == 2:
                jahr = datetime.datetime.strptime(str(jahr), "%y")
                jahr = str(jahr)[:4]

        result_line_kw = pattern_kw.match(line)
        if result_line_kw is not None:
            kw = result_line_kw.group(1)
            line = result_line_kw.group(2)
            result_line_seperator = pattern_seperator.match(line)
            if result_line_seperator is not None: 
                line = result_line_seperator.group(1)

        result_line_weekday = pattern_weekday.match(line)
        if result_line_weekday is not None:
            weekday = result_line_weekday.group(1)
            line = result_line_weekday.group(2)
            for daypattern in Weekdays:
                if weekday in daypattern:
                    dt = epoch_to_dates.epoch_to_datetime_message(jahr, kw, weekday)
                    print(dt)
                elif weekday not in daypattern:
                    continue

        if len(lines) == 1 and result_line_kw is not None:
            monday, tuesday, wednesday, thursday, friday = epoch_to_dates.kw_to_dates(jahr, kw)
            print(monday + "|" + tuesday + "|" + wednesday + "|" + thursday + "|" + friday)
            

def iterate_message_lines(event_message_text):
    return event_message_text.splitlines()

class epoch_to_dates:
    def kw_to_dates(jahr, kw):
        monday = datetime.datetime.strptime(f'{jahr}-W{int(kw)}-1', "%Y-W%W-%w").date()
        tuesday = monday + datetime.timedelta(days=1)
        wednesday = monday + datetime.timedelta(days=2)
        thursday = monday + datetime.timedelta(days=3)
        friday = monday + datetime.timedelta(days=4)
        return str(monday), str(tuesday), str(wednesday), str(thursday), str(friday)

    def epoch_to_datetime_message(jahr, kw, weekday):
        jahr = str(jahr)
        kw = str(kw)
        weekday = str(weekday)
        if len(weekday) == 2:
            locale.setlocale(locale.LC_ALL, "de_DE.utf8")
            dt = datetime.datetime.strptime(str(jahr) + "-" + str(kw) + "-" + str(weekday), "%Y-%W-%a")
            locale.setlocale(locale.LC_ALL, "")
            return dt
        if len(weekday) == 3:
            dt = datetime.datetime.strptime(str(jahr) + "-" + str(kw) + "-" + str(weekday), "%Y-%W-%a")
            return dt
        if "day" in weekday:
            dt = datetime.datetime.strptime(str(jahr) + "-" + str(kw) + "-" + str(weekday), "%Y-%W-%A")
            return dt
        elif "day" not in weekday and len(weekday) > 3:
            locale.setlocale(locale.LC_ALL, "de_DE.utf8")
            dt = datetime.datetime.strptime(str(jahr) + "-" + str(kw) + "-" + str(weekday), "%Y-%W-%A")
            locale.setlocale(locale.LC_ALL, "")
            return dt
        else:
            print("Nothing") 

    def event_ts_date(event):
        ts = event.get("ts")
        timestamp = datetime.datetime.fromtimestamp(float(ts))
        year1 = str(timestamp)[0:4]
        month1 = str(timestamp)[5:7]
        day1 = str(timestamp)[8:10]
        calendar_week = datetime.date(int(year1), int(month1), int(day1)).isocalendar()[1]
        Day_of_the_week = datetime.date(int(year1), int(month1), int(day1)).isocalendar()[2]
        return int(year1), calendar_week, Day_of_the_week

def fetch_history_messages(event):
    channel_id = event.get("channel")
    ts = event.get("ts")
    client_history = client.conversations_history(channel=channel_id, oldest=1630308.933000, latest=ts, inclusive= True, limit= 1000000)    
    return client_history.get("messages", {})
    
def handle_message(message):
    text = message.get("text")
    timestamp = message.get("ts")
    user = message.get("user")
    return timestamp, text, user

if __name__ == "__main__":
    slack_event_adapter.start(
        port=8080, host="0.0.0.0")
    
