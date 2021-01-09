import speech_recognition as sr

class VirtualAssistant:
    def __init__(self, listener, mic, engine):
        self.listener = listener
        self.mic = mic
        self.engine = engine

    def introduce(self):
        self.engine.say("Hello, I am your assistant Alfred")
        self.engine.say("What would you like to do?")
        self.engine.runAndWait()

    def get_user_command(self) -> str:
        try:
            with self.mic as source:
                listener = self.listener

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