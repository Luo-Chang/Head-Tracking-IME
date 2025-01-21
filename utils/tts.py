import win32com.client as wincom
import time
import threading

speak = wincom.Dispatch("SAPI.SpVoice")

# List all available voices
voices = speak.GetVoices()
for voice in voices:
    print(voice.GetDescription())

# Set the voice to Chinese (if available)
for voice in voices:
    if "Chinese" in voice.GetDescription() or "中文" in voice.GetDescription() or "汉语" in voice.GetDescription() or "普通话" in voice.GetDescription():
        speak.Voice = voice
        break

def invoke_tts(text):
    speak.Speak(text)
    
    
if __name__=="__main__":
    text = "你好吗"
    invoke_tts(text)

    # 3 second sleep
    time.sleep(3) 

    text = "This text is read after 3 seconds"
    invoke_tts(text)
