import speech_recognition as sr
import pyttsx3


def audio_to_text(recognizer, mic):
	if not isinstance(recognizer, sr.Recognizer):
		raise TypeError("recognizer must be speech_recognition.Recognizer instance")
	
	if not isinstance(mic, sr.Microphone):
		raise TypeError("mic must be speech_recognition.Microphone instance")
	
	result = { "success": True, "input": None }
	
	with mic as source:
		recognizer.adjust_for_ambient_noise(source, duration = 1)
		audio_input = recognizer.listen(source)
		try:
			result["input"] = recognizer.recognize_google(audio_input)
		except sr.UnknownValueError:
			result["input"] = None
		except sr.RequestError:
			result["success"] = False
			result["input"] = "speech recognition Google API is unavailable"
	
	return result

def speak(text):
	speech = pyttsx3.init()
	voices = speech.getProperty('voices')
	speech.setProperty("voice", voices[2].id)
	speech.setProperty('rate', 125)
	speech.say(text)
	speech.runAndWait()

def main():
	print("Speech recognition software version: " + sr.__version__)

	r = sr.Recognizer()
	mic = sr.Microphone(device_index = 1) # if no device_index supplied, then default mic (i'm not using the default one atm)
	
	while True:
		result = audio_to_text(r, mic)
		if not result["success"]:
			print("Technical problems: " + result["input"])
			break
		elif result["input"] == None:
			print("Sorry, I did not hear you")
		else:
			print("You said: " + result["input"])
			speak(result["input"])

main()