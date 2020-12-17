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