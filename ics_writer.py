# Need to write unit testing for this file. Make sure to cover 100%. Check where the file gets saved.
from typing import Tuple
from pathlib import Path

def to_ics(event: dict) -> Tuple[str, str]:
    '''
    Creates a string with all the information provided from the event dictionary to develop an ICS file.
    An ICS file eases the process of adding an event to your digital calendar.
    Input: event, a dictionary containing all the information for the development of the ICS file.
    Return: ics_string, a string containing the information to be added into an .ics file.
            filename, a string containing the title of the ics file.
    '''
    ics_string = ("BEGIN:VCALENDAR\r\n"
                "VERSION:2.0\r\n"
                "PRODID:-//LabHelperBot//CalendarExport 1.0//EN\r\n"
                "BEGIN:VEVENT\r\n")
    ics_string += "UID:" + event['uid'] + "\r\n"
    ics_string += "DTSTAMP:" + event['date'] + "T" + event['start_time'] + "Z\r\n"
    ics_string += "DTSTART:" + event['date'] + "T" + event['start_time'] + "\r\n"
    ics_string += "DTEND:" + event['date'] + "T" + event['end_time'] + "\r\n"
    ics_string += "SUMMARY:" + event['title'] + "\r\n"
    ics_string += "DESCRIPTION:" + event['description'] + "\r\n"
    ics_string += "LOCATION:" + event['location'] + "\r\n"
    for email in event['emails']:
        ics_string += "ATTENDEE;CN=" + email + ":mailto:" + email + "\r\n"
    ics_string += "END:VEVENT\r\n"
    ics_string += "END:VCALENDAR\r\n"

    return ics_string, event['title'].replace(" ", "")


def ics_writer(event: dict) -> str:
    '''
    Creates an .ics file.
    Input: ics_string, the string responsible for having all of the information to write an ics file.
    '''
    ics_string, filename = to_ics(event)
    filepath = Path(f"{filename}.ics")

    with filepath.open('w') as file:
        file.write(ics_string)
    
    return str(filepath)