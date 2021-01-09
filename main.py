import speech_recognition_api as sr

# Setup speech recognition and text-to-speech engine
listener = sr.setup_speech_recognizer()
engine = sr.setup_engine()

# Setup microphone and listen
mic = sr.setup_microphone()

# Create virtual assistant
assistant = sr.create_virtual_assistant(listener, mic, engine)
assistant.introduce()

# Retrieve and execute command
while 1:
    action = sr.get_reminder_action(assistant)
    reminders = sr.execute_action(assistant, action)
    print(reminders)
    engine.say(reminders)
    engine.runAndWait()
