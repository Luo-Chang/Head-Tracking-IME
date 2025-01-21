import win32com.client as wincom
import time

speak = wincom.Dispatch("SAPI.SpVoice")

# List all available voices
voices = speak.GetVoices()
for voice in voices:
    print(voice.GetDescription())

# Set the voice to Chinese (if available)
for voice in voices:
    if "Chinese" in voice.GetDescription():
        speak.Voice = voice
        break

def invoke_tts(text):
    speak.Speak(text)
    

if __name__=="__main__":
    text = "你好吗"
    speak.Speak(text)

    # 3 second sleep
    time.sleep(3) 

    text = "This text is read after 3 seconds"
    speak.Speak(text)
