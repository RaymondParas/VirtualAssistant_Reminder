import requests
from datetime import datetime as dt

BASE = "http://127.0.0.1:5000/"

def get_reminders():
    reminder_text = "Sorry, there seems to be an issue with the service"

    try:
        response = requests.get(BASE + "reminder")
    except Exception as error:
        print(error)
        return reminder_text

    if (response.status_code == 200):
        reminder_text = ''
        reminders = response.json()
        if len(reminders) == 0:
            return "You do not have any reminders currently"
        for reminder in reminders:
            reminder_text += f"You have a {reminder['name']}"
            if reminder['address'] is not None:
                reminder_text += f" appointment at {reminder['address']}"
            if reminder['appointment'] is not None:
                appointment_date = dt.strptime(reminder['appointment'], '%a, %d %b %Y %H:%M:%S -%f').strftime('%A, %B %d at %I:%M %p')
                reminder_text += f" on {appointment_date}"
            if (reminder != reminders[-1]):
                reminder_text += "\n"

    return reminder_text

def add_reminder(body):
    reminder_text = "Sorry, there seems to be an issue with the service"
    try:
        response = requests.post(BASE + "reminder", body)
    except Exception as error:
        print(error)
        return reminder_text

    if (response.status_code == 200):
        reminder_text = "The reminder was added"

    return reminder_text

def delete_reminder(body):
    reminder_text = "Sorry, there seems to be an issue with the service"
    try:
        response = requests.delete(BASE + "reminder", data=body)
    except Exception as error:
        print(error)
        return reminder_text

    if (response.status_code == 200):
        reminder_text = "The reminder was deleted"

    return reminder_text