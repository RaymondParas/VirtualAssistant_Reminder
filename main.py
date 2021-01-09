import speech_recognition_api as sr

# Setup speech recognition and text-to-speech engine
listener = sr.setup_speech_recognizer()
engine = sr.setup_engine()

# Setup microphone and listen
mic = sr.setup_microphone()

# Retrieve and execute command
while 1:
    action = sr.get_reminder_action(listener, mic)
    reminders = sr.execute_action(listener, mic, engine, action)
    print(reminders)
    engine.say(reminders)
    engine.runAndWait()
