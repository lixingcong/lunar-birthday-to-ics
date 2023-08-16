#!/usr/bin/env python3

import argparse
import datetime
import ics
import lunarcalendar
import json
import os
import sys

# Global vars
KEY_PERSONS='persons'
KEY_NAME = 'name'
KEY_BIRTHDAY_SOLAR = 'birthday'
KEY_BIRTHDAY_LUNAR = 'birthday_lunar'

def die(err):
    sys.exit(err)

def json_to_persons(json_file_path):
    ret = []
    with open(json_file_path, 'r') as f:
        json_object = json.load(f)
        if KEY_PERSONS in json_object:
            for person in json_object[KEY_PERSONS]:
                if KEY_NAME not in person:
                    die(f'missing key {KEY_NAME} in {json_file_path}')
                
                if KEY_BIRTHDAY_SOLAR not in person:
                    die(f'missing key {KEY_BIRTHDAY_SOLAR} in {json_file_path}')
                
                birthday_solar = datetime.datetime.strptime(person[KEY_BIRTHDAY_SOLAR], '%Y-%m-%d')
                birthday_luna = lunarcalendar.Converter.Solar2Lunar(lunarcalendar.Solar(birthday_solar.year, birthday_solar.month, birthday_solar.day))

                person[KEY_BIRTHDAY_SOLAR] = birthday_solar
                person[KEY_BIRTHDAY_LUNAR] = birthday_luna
                ret.append(person)                                    
        else:
            die(f'missing key {KEY_PERSONS} in {json_file_path}')
    return ret

def append_birthday_to_calendar(calendar, solar_year, lunar_month, lunar_day, name, age):
    new_birthday_solars = []

    # birthday which is not leap month
    new_birthday_lunar = lunarcalendar.Lunar(solar_year, lunar_month, lunar_day, isleap = False)
    new_birthday_solars.append(lunarcalendar.Converter.Lunar2Solar(new_birthday_lunar))

    # birthday which is leap month
    try:
        new_birthday_lunar = lunarcalendar.Lunar(solar_year, lunar_month, lunar_day, isleap = True)
        new_birthday_solars.append(lunarcalendar.Converter.Lunar2Solar(new_birthday_lunar))
        # print(f'There is a leap month in {solar_year}-{lunar_month}')
    except lunarcalendar.DateNotExist:
        # print(f'Not exist for leap month in {solar_year}-{lunar_month}')
        pass

    for i in range(len(new_birthday_solars)):
        new_birthday_solar = new_birthday_solars[i]

        icsEvent = ics.Event()
        icsEvent.name = f'{name}的农历{age}岁生日'
        if i > 0:
            icsEvent.name += '(闰)'
        icsEvent.description = f'生日快乐，公历{birthday_solar_year}年出生，农历{lunar_month:02d}-{lunar_day:02d}'
        icsEvent.begin = datetime.datetime(new_birthday_solar.year, new_birthday_solar.month, new_birthday_solar.day)
        icsEvent.make_all_day()
        icsEvent.created = datetime.datetime.now()
        calendar.events.add(icsEvent)

if __name__ == "__main__":
    script_file = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(prog=script_file,
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80),
                                     description='A simple script to generate chinese lunar calendar birthday')
    parser.add_argument('-i', metavar='config.json', help='The input config file', required=True)
    parser.add_argument('-c', metavar='COUNT', help='The number of occurrences(in years), default value: 50', default=50, type=int)

    args = vars(parser.parse_args())
    # print(args)

    json_file_path = args['i']
    event_count = args['c']
    
    persons = json_to_persons(json_file_path)
    # print(persons)

    calendar = ics.Calendar()
    event_steps = list(range(event_count))
    today_solar_year = datetime.datetime.today().year
    
    for person in persons:
        birthday_lunar = person[KEY_BIRTHDAY_LUNAR]
        birthday_lunar_month = birthday_lunar.month
        birthday_lunar_day = birthday_lunar.day
        birthday_solar_year = person[KEY_BIRTHDAY_SOLAR].year
        name = person[KEY_NAME]
        
        for step in event_steps:
            solar_new_year = today_solar_year + step
            age = solar_new_year - birthday_solar_year
            if age >= 0:           
                append_birthday_to_calendar(calendar, solar_new_year, birthday_lunar_month, birthday_lunar_day, name, age)

    print(calendar.serialize())