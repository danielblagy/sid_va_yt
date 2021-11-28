import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
from subprocess import Popen, CREATE_NEW_CONSOLE
import random
import sys


speech = 0

commands = {}
scripts = {}
responses = {}

active = True


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
	speech.say(text)
	speech.runAndWait()
	
def read_entire_file(filepath):
	try:
		file = open(filepath, "r")
		file_contents = file.read()
		file.close()
		
		return file_contents
	except IOError:
		print("Couldn't read " + filepath)
		exit

def get_resource(resource_path):
	file_contents = read_entire_file(resource_path)

	resource = {}

	lines = file_contents.split("\n")
	for line in lines:
		resource_item = line.split(" : ")
		resource.update({resource_item[0] : resource_item[1].split(",")})
	
	return resource
	
def match(command_type, words):
	for vocab_word in commands[command_type]:
		if vocab_word in words:
			return True
	return False
	
def react(input):
	if active:
		if match("search", input):
			execute_search_command(input)
		elif match("start", input):
			execute_start_command(input)
		elif match("time", input):
			execute_time_command()
		elif match("weather", input):
			execute_weather_command()
		elif match("hello", input):
			execute_greet_command()
		elif match("bye", input):
			execute_bye_command()
		elif match("thanks", input):
			execute_thanks_command()
		elif match("sleep", input):
			execute_sleep_command()
	else:
		if match("wake", input):
			execute_wake_command()

def execute_wake_command():
	speak("I'm here")
	global active
	active = True
	
def execute_sleep_command():
	speak("Going to sleep")
	global active
	active = False
	
def execute_time_command():
	current_time = datetime.now()
	speak("It's " + current_time.strftime("%H:%M %A %d of %B %Y"))
	print("It's ", current_time.strftime("%H:%M %A %d of %B %Y"))

def execute_search_command(words):
	speak("Opening in the browser")
	query = "robot ai uprising"
	
	for vocab_word in commands["search"]:
		if vocab_word in words:
			query = words[len(vocab_word) + 1:] # substring with only query in it ('+ 1' for one space)
			break
	
	url = "https://www.google.com/search?q={}".format(query)
	webbrowser.open(url)
	
def execute_weather_command():
	execute_search_command("search weather")
	
def execute_greet_command():
	response = responses["hello"]
	speak(response[random.randint(0, len(response) - 1)])

def execute_bye_command():
	response = responses["bye"]
	speak(response[random.randint(0, len(response) - 1)])
	sys.exit()

def execute_thanks_command():
	response = responses["thanks"]
	speak(response[random.randint(0, len(response) - 1)])
	
def execute_start_command(words):
	# occasionaly sid will give a response
	# P = 0.5 * 0.5 * 0.5 = 0.125, i.e. the response will be given in 12.5% of the occurences
	if (random.randint(0, 1) + random.randint(0, 1) + random.randint(0, 1)) == 3:
		speak(responses["ok"][random.randint(0, len(responses["ok"]) - 1)])

	for script_name in scripts.keys():
		if script_name in words:
			for script_command in scripts[script_name]:
				Popen(script_command, stdin=None, stdout=None, stderr=None, shell=True, creationflags=CREATE_NEW_CONSOLE)
			break

def main():
	r = sr.Recognizer()
	mic = sr.Microphone(device_index = 1) # if no device_index supplied, then default mic (i'm not using the default one atm)
	
	global speech
	
	speech = pyttsx3.init()
	voices = speech.getProperty('voices')
	speech.setProperty("voice", voices[2].id)
	speech.setProperty('rate', 125)
	
	global commands
	global scripts
	global responses
	
	commands = get_resource("resources/commands.sid")
	scripts = get_resource("resources/start_scripts.sid")
	responses = get_resource("resources/responses.sid")
	
	while True:
		result = audio_to_text(r, mic)
		if not result["success"]:
			print("Technical problems: " + result["input"])
			break
		elif result["input"] == None:
			print("words could not be discerned")
		else:
			print("You said: " + result["input"])
			react(result["input"])

main()