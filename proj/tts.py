import win32com.client as wincom
import time

speak = wincom.Dispatch("SAPI.SpVoice")

text = "你好吗"
speak.Speak(text)

# 3 second sleep
time.sleep(3) 

text = "This text is read after 3 seconds"
speak.Speak(text)
