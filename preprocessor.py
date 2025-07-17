# In preprocess.py

import pandas as pd
import re


def preprocess(data):
    # This pattern works for both 12-hour and 24-hour time formats from WhatsApp
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:[ap]m\s)?-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Check if lists are of the same length
    if len(messages) != len(dates):
        # Handle the case where splitting results in unequal lists, maybe return empty df
        return pd.DataFrame()

    df = pd.DataFrame({'user_msg': messages, 'message_date': dates})

    # A more robust way to parse dates
    try:
        # Try parsing with day-first format (e.g., 11/03/2023 -> March 11)
        df['date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    except ValueError:
        # If that fails, try parsing with month-first format (e.g., 3/11/2023 -> March 11)
        # Note the change from %d/%m to %m/%d
        df['date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M %p - ')

    users = []
    messages = []
    for msg in df['user_msg']:
        # This regex correctly handles user names that may contain spaces
        entry = re.split(r'([\w\s]+?):\s', msg)
        if len(entry) > 2 and entry[1] and entry[2]:  # Check if split is valid
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_msg'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df.drop(columns=['date','message_date'],inplace=True)
    # Return the final, cleaned DataFrame
    return df