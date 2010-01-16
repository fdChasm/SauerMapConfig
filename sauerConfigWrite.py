def configwrite(datastructure):
	def determine_shader_type(texturedata):
		tdglist = []
		for key in ["0file","dfile","nfile","sfile","gfile","zfile"]:
			if texturedata[key] != "":
				tdglist.append(key[0])
		print tdglist
		tdglist.sort()
		print tdglist

		if tdglist == ["0"]:
			return "stdworld"
		elif tdglist == ['0', 'd']:
			return "decalworld"

	def build_texture_lines(texturedata, shadertype):
		returnlist2 = []
		for rotationtype in texturedata['rotated'].keys():
			for rotation in texturedata['rotated'][rotationtype][1].keys():
				tdg = return_texture_desig_list(shadertype)
				for tdgi in tdg:
					tdgikey = tdgi + "file"
					appendline = "texture " + tdgi + " \"" + texturedata[tdgikey] + "\" " + return_rottype(rotationtype) + " " + str(texturedata['rotated'][rotationtype][1][rotation][0]) + " " + str(texturedata['rotated'][rotationtype][1][rotation][1]) + " " + str(texturedata['rotated'][rotationtype][1][rotation][2]) + "\n"
					returnlist2.append(appendline)
		return returnlist2

	def return_texture_desig_list(shadertype):
		if shadertype == "stdworld":
			returnlist = ["0"]
		elif shadertype == "decalworld":
			returnlist = ['0', 'd'] 
		return returnlist

	def return_rottype(rotationtype):
		if rotationtype == "norot":
			return "0"
		elif rotationtype == "90cw":
			return "1"
		elif rotationtype == "180cw":
			return "2"
		elif rotationtype == "270cw":
			return "3"
		elif rotationtype == "xax":
			return "4"
		elif rotationtype == "yax":
			return "5"
	
	
	returnlist = []
	title = datastructure["title"]
	atitle = "// Config file for map:" + title + "\n"
	author = datastructure["author"]
	aauthor = "// By:" + author + "\n\n"
	data = datastructure["datatree"]

	shaders = {}
	shaders["stdworld"] = []
	shaders["decalworld"] = []

	for texture in data.keys():
		textureshader = determine_shader_type(data[texture])
		shaders[textureshader].append(texture)


	returnlist.append(atitle)
	returnlist.append(aauthor)

	returnlist.append("texturereset\n")
	returnlist.append("texture 0 \"ik2k/ik_sky_day_back.jpg\"\n")
	returnlist.append("texture 0 \"golgotha/water2d.jpg\"\n\n")

	for shadertype in shaders.keys():
		shaderappend = "setshader " + shadertype + "\n"
		if shaders[shadertype] != []:
			returnlist.append(shaderappend)
		for texturename in shaders[shadertype]:
			textureappend_lines = build_texture_lines(data[texturename], shadertype)
			for textureappend in textureappend_lines:
				returnlist.append(textureappend)



	print datastructure
	return returnlist
