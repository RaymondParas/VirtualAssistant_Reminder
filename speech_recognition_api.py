import sys
import speech_recognition as sr
import pyttsx3
from reminder_api import get_reminders, add_reminder, delete_reminder

get_keywords = ['get', 'tell', 'show', 'give']
post_keywords = ['add', 'create']
put_keywords = ['update', 'modify']
delete_keywords = ['delete', 'remove', 'erase']
keywords = get_keywords + post_keywords + put_keywords + delete_keywords

terminate_keywords = ['stop alfred', 'turn off alfred']
reminder_api_keyword = "reminder"

def setup_speech_recognizer():
    return sr.Recognizer()

def setup_microphone():
    return sr.Microphone()

def print_microphones():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def setup_engine():
    engine = pyttsx3.init()
    engine.say("Hello, I am your assistant Alfred")
    engine.say("What would you like to do?")
    engine.runAndWait()
    return engine

def get_user_command(mic, listener) -> str:
    try:
        with mic as source:
            listener.pause_threshold=1
            listener.adjust_for_ambient_noise(source,duration=0.5) 

            print('Listening...')
            voice = listener.listen(source, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            
            print(command)
            return str(command.lower())
    except Exception as e:
        print(e)
        return None

def get_reminder_command(listener, mic):
    command_key = None
    while(command_key == None or not any(keyword in command_key for keyword in keywords) or reminder_api_keyword not in command_key):
        command_key = get_user_command(mic, listener)
        if command_key != None:
            terminate_app(command_key)
    return command_key

def terminate_app(command):
    if any(keyword in command for keyword in terminate_keywords):
            print("Terminating...")
            sys.exit()

def execute_command(listener, mic, engine, command):
    if (any(keyword in command for keyword in get_keywords)):
        return get_reminders()
    elif (any(keyword in command for keyword in post_keywords)):
        reminder_to_create = build_reminder(listener, mic, engine)
        return add_reminder(reminder_to_create)
    elif (any(keyword in command for keyword in put_keywords)):
        return "The reminder was updated"
    elif (any(keyword in command for keyword in delete_keywords)):
        reminder_to_delete = build_delete_reminder_model(listener, mic, engine)
        return delete_reminder(reminder_to_delete)
    else:
        return 'Unrecognized command'

def get_command_keyword(listener, mic):
    command_key = None
    while(command_key == None or command_key == ''):
        command_key = get_user_command(mic, listener)
        if command_key != None:
            terminate_app(command_key)
    return command_key

def ask_and_receive_command(listener, mic, engine, message):
    engine.say(message)
    engine.runAndWait()
    command = get_command_keyword(listener, mic)
    return command

def build_reminder(listener, mic, engine):
    reminder = {}
    message = "Sure, what for?"
    data = ask_and_receive_command(listener, mic, engine, message)
    reminder['name'] = data

    message = "Would you like to add any additional information?"
    data = ask_and_receive_command(listener, mic, engine, message)
    return reminder

def build_delete_reminder_model(listener, mic, engine):
    reminder_to_delete = {}
    message = "Which reminder would you like to delete?"
    data = ask_and_receive_command(listener, mic, engine, message)
    reminder_to_delete['name'] = data
    return reminder_to_delete
