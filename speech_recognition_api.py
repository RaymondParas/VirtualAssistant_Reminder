import sys
import speech_recognition as sr
import pyttsx3
from reminder_api import get_reminders, add_reminder, delete_reminder

# Keywords for each request method
get_keywords = ['get', 'tell', 'show', 'give', 'read']
post_keywords = ['add', 'create']
put_keywords = ['update', 'modify']
delete_keywords = ['delete', 'remove', 'erase']

# All user keywords to listen for
keywords = get_keywords + post_keywords + put_keywords + delete_keywords
reminder_api_keyword = "reminder"

# Keywords for terminating program
terminate_keywords = ['stop alfred', 'turn off alfred']

# Keywords for proceeding with a process
proceed_keywords = ['yes', 'sure', 'yeah', ' yup']

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
            # Calibrate energy threshold for 1 second
            listener.adjust_for_ambient_noise(source)

            # Listen for maximum of 5 seconds then recognize using Google API
            print('Listening...')
            listener.pause_threshold=1
            voice = listener.listen(source, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            
            # Return as lowercase string
            lower_case_command = str(command).lower()
            print(lower_case_command)
            return lower_case_command
    except sr.UnknownValueError:
        print("No speech detected")
        return None
    except sr.RequestError:
        print("ERROR: Google Recognizer API is unavailable")
        return None

def get_until_command_is_valid(listener, mic):
    command_key = None
    while(command_key is None or command_key == ''):
        command_key = get_user_command(mic, listener)
        if command_key is not None:
            terminate_app(command_key)
    return command_key

def terminate_app(command):
    if any(keyword in command for keyword in terminate_keywords):
            print("Terminating...")
            sys.exit()

def get_reminder_action(listener, mic):
    command = None
    action = None
    while(command is None or action is None or reminder_api_keyword not in command):
        command = get_user_command(mic, listener)
        if command is not None:
            terminate_app(command) # Terminate if condition is true, else ignore
            action = next((keyword for keyword in keywords if keyword in command), None)
    return action

def execute_action(listener, mic, engine, action):
    if action in get_keywords:
        return get_reminders()
    elif action in post_keywords:
        reminder_to_create = build_reminder_model(listener, mic, engine)
        return add_reminder(reminder_to_create)
    elif action in put_keywords:
        return "The reminder was updated"
    elif action in delete_keywords:
        reminder_to_delete = build_delete_reminder_model(listener, mic, engine)
        return delete_reminder(reminder_to_delete)
    else:
        return 'Unrecognized command'

def ask_and_receive_command(listener, mic, engine, message):
    engine.say(message)
    engine.runAndWait()
    command = get_until_command_is_valid(listener, mic)
    return command

def build_reminder_model(listener, mic, engine):
    reminder = {}
    first_iteration = True
    while (reminder == {}):
        message = "Sure, what for?" if first_iteration is True else "Can you repeat the name?"
        first_iteration = False

        data = ask_and_receive_command(listener, mic, engine, message)
        message = f"Is {data} correct?"
        response = ask_and_receive_command(listener, mic, engine, message)
        if any(keyword in response for keyword in proceed_keywords):
            reminder['name'] = data

    return reminder

def build_delete_reminder_model(listener, mic, engine):
    reminder_to_delete = {}
    message = "Which reminder would you like to delete?"
    data = ask_and_receive_command(listener, mic, engine, message)
    reminder_to_delete['name'] = data
    return reminder_to_delete
