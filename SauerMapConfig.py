#standard classes
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk
from copy import deepcopy
import cPickle, os, time, tkMessageBox, ConfigParser, string

#custom classes
from custom_classes import *
import tkSimpleDialog
import tkDispModWidget
from tkImageSelectionButtonWithClear import tkImageSelectionButtonWithClear
import sauerConfigWrite

##########################################################################################################
#PRE	:Takes no input
#POST	:returns a guess at what opperating system it was run on
def clear_screen():
	if os.name == "posix":
		os.system('clear')
	elif os.name == "nt":
		os.system('CLS')
	else:
		print "\n"*100
##########################################################################################################
#PRE	:takes a string with a set of parentheses somewhere in it
#POST	:returns what is between the two parentheses
def item_between_perentheses(string):
	readinto = False
	returnstring = ""
	for letter in string:
		if letter == ")":
			readinto = False
		if readinto:
			returnstring += letter
		if letter == "(":
			readinto = True
	#print "will return:", returnstring
	return returnstring

##########################################################################################################
class App:
	def __init__(self, master):
		master.protocol("WM_DELETE_WINDOW", self.onclose_callback)

		master.title('Sauerbraten cfg creator')
		#master.minsize(486,168)
		master.resizable(width=FALSE, height=FALSE)
		
		self.parent = master
		self.PROJECT = Project()
		self.initializecurrenttexvariables()

		# create a toplevel menu
		self.menubar = Menu(master)
		self.createmenu()
		# display the menu
		master.config(menu=self.menubar)
		
		#window list of textures
		self.mainframe = Frame(master)
		
		self.scrollbar = Scrollbar(self.mainframe, orient=VERTICAL)
		self.listbox = Listbox(self.mainframe, yscrollcommand=self.scrollbar.set, selectmode = SINGLE, width=70, exportselection=0)
		self.listbox.bind("<ButtonRelease-1>", self.texture_onclick)

		self.scrollbar.config(command=self.listbox.yview)

		self.scrollbar.grid(row=0, column=2, sticky='wnes')
		self.listbox.grid(row=0, column=0, sticky=W+E+N+S)

		#texture cofiguration
		self.texture_configuration_frame = LabelFrame(master, text = "No texture selected")
		

		self.build_texture_selection_buttons()


		#define the rotations selections spinboxes
		self.spinbox_rotation_frame = Frame(self.texture_configuration_frame, borderwidth=1)
		self.build_rotation_selections()
		self.spinbox_rotation_frame.grid(row = 1, column = 2, sticky = 'nsew')
		


		#which rotation to change displacement on
		self.displaceframe = Frame(self.texture_configuration_frame, width = 144, borderwidth=1)
		self.rotselframe = Frame(self.displaceframe, width = 10, height = 10)
		self.rotselscrollbar = Scrollbar(self.rotselframe, orient=VERTICAL)
		self.rotsellistbox = Listbox(self.rotselframe, yscrollcommand=self.rotselscrollbar.set, selectmode = SINGLE, exportselection=0)
		self.rotsellistbox.bind("<ButtonRelease-1>", self.tex_rotver_onclick)
		self.rotselscrollbar.config(command=self.rotsellistbox.yview)
		self.rotselscrollbar.pack(side=RIGHT, fill=Y)
		self.rotsellistbox.config(width  = 22, height = 7)
		self.rotsellistbox.pack(side=LEFT)
		self.rotselframe.grid(row = 1, column = 1, sticky = 'snew')
		#Controls for modifying the offsets of the various texture rotations

		self.dispmod = tkDispModWidget.tkDispModWidget(self.displaceframe)
		self.dispmod.config(command=lambda: self.offset_conf_onclick("item"))
		self.dispmod.grid(row = 2, column = 1, sticky = 'snew')

		self.displaceframe.grid(row = 1, column = 3, sticky = 'snew')


		if self.tex_list_sel == () or self.tex_name == "No texture selected":
			self.texture_configuration_frame.grid_forget()
		else:
			self.texture_configuration_frame.grid()
		self.texture_configuration_frame.config(text = self.tex_name)



		self.mainframe.grid(sticky = W+E+N+S)

#######################################################################################################################
####MISC###############################################################################################################
#######################################################################################################################

	##########################################################################################################
	#PRE	:
	#POST	:
	def onclose_callback(self):
		#if tkMessageBox.askokcancel("Quit", "There may be Unsaved data!\nDo you really wish to quit?"):
		self.parent.destroy()

	##########################################################################################################
	#PRE	:
	#POST	:
	def initializecurrenttexvariables(self):
		self.tex_list_sel = ()
		self.rot_list_sel = ()
		self.tex_name = "No texture selected"
		self.rot_name = "No rotation selected"
		
#######################################################################################################################
####BUILD GUI COMPONENTS###############################################################################################
#######################################################################################################################



	##########################################################################################################
	#PRE	:
	#POST	:
	def build_texture_selection_buttons(self):
		#textureselection goes here
		###################
		self.texture_selection_frame = Frame(self.texture_configuration_frame, width = 144, borderwidth=1)
		self.notexturehandle = Image.open("notexture.png")
		self.notex = self.notexturehandle.resize((40, 40), Image.BICUBIC)
		self.notexture = ImageTk.PhotoImage(self.notex)
		# create the image buttons, image is above
		self.texture_selection_button_images = {}
		self.texture_selection_buttons = {}
		self.texture_selection_buttons["0file"] = tkImageSelectionButtonWithClear(self.texture_selection_frame, compound=TOP, width=64, height=64, text="tex_0")
		self.texture_selection_buttons["dfile"] = tkImageSelectionButtonWithClear(self.texture_selection_frame, compound=TOP, width=64, height=64, text="tex_d")
		self.texture_selection_buttons["nfile"] = tkImageSelectionButtonWithClear(self.texture_selection_frame, compound=TOP, width=64, height=64, text="tex_n")
		self.texture_selection_buttons["sfile"] = tkImageSelectionButtonWithClear(self.texture_selection_frame, compound=TOP, width=64, height=64, text="tex_s")
		self.texture_selection_buttons["gfile"] = tkImageSelectionButtonWithClear(self.texture_selection_frame, compound=TOP, width=64, height=64, text="tex_g")
		self.texture_selection_buttons["zfile"] = tkImageSelectionButtonWithClear(self.texture_selection_frame, compound=TOP, width=64, height=64, text="tex_z")

		brow = 1
		bcolumn = 1
		for button in self.texture_selection_buttons.keys():
			self.texture_selection_button_images[button] = self.notexture
			self.texture_selection_buttons[button].grid(row = brow, column = bcolumn, sticky = 'snew', padx=2, pady=2)
			self.texture_selection_buttons[button].config(image=self.texture_selection_button_images[button], command=lambda b=button:self.modtexfilepath(b), xcommand=lambda b=button:self.blanktexfilepath(b))
			brow += 1
			if brow > 3:
				bcolumn = 2
				brow = 1
		self.refresh_texture_buttons()
		self.texture_selection_frame.grid(row = 1, column = 1, sticky = 'snew')


	##########################################################################################################
	#PRE	:
	#POST	:
	def createmenu(self):
		self.projectmenu = Menu(self.menubar, tearoff=0)
		self.projectmenu.add_command(label="New", command=self.new_project)
		self.projectmenu.add_command(label="Open", command=self.open_project)
		self.projectmenu.add_command(label="Save", command=self.save_project)
		self.projectmenu.add_command(label="Save As", command=self.saveas_project)
		self.projectmenu.add_separator()
		self.projectmenu.add_command(label="Properties", command=self.properties_project)
		self.projectmenu.add_separator()
		self.projectmenu.add_command(label="Exit", command=root.quit)
		self.menubar.add_cascade(label="Project", menu=self.projectmenu)

		self.texmenu = Menu(self.menubar, tearoff=0)
		self.texmenu.add_command(label="New texture", command=self.add_newtex)
		self.texmenu.add_command(label="Delete texture", command=self.removetex)
		self.texmenu.add_command(label="Texture properties", command=self.tex_prop_menu_item)
		self.menubar.add_cascade(label="Texture", menu=self.texmenu)

		self.toolsmenu = Menu(self.menubar, tearoff=0)
		self.toolsmenu.add_command(label="Export to cfg", command=self.exportcfg)
		self.toolsmenu.add_command(label="Preferenes", command=self.generalconfig)
		self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

		self.helpmenu = Menu(self.menubar, tearoff=0)
		self.helpmenu.add_command(label="About", command=self.about)
		self.menubar.add_cascade(label="Help", menu=self.helpmenu)

	##########################################################################################################
	#PRE	:
	#POST	:
	def build_rotation_selections(self):
		rot_lines = ["norot", "90cw", "180cw", "270cw", "xax", "yax"]
		self.rotspin = {}
		for line in rot_lines:
			self.rotspin[line] = {}
			self.rotspin[line]["var"] = IntVar()
			self.rotspin[line]["label"] = Label(self.spinbox_rotation_frame, text=line)
			self.rotspin[line]["spinbox"] = Spinbox(self.spinbox_rotation_frame, width= 2, from_=0, to=10, command=self.rot_spin_onclick, textvariable=self.rotspin[line]["var"])
		#place them on the grid
		therow = 1
		for line in self.rotspin.keys():
			self.rotspin[line]["label"].grid(row = therow, column = 1, sticky = 'nw')
			self.rotspin[line]["spinbox"].grid(row = therow, column = 2, sticky = 'ne')
			therow = therow + 1

#######################################################################################################################
####REFRESHES##########################################################################################################
#######################################################################################################################

	##########################################################################################################
	#PRE	:
	#POST	:
	def refresh_texture_buttons(self):
		print "refresh_texture_buttons ran"
		for button in self.texture_selection_buttons.keys():
			#print self.get_butimg(button)
			self.texture_selection_button_images[button] = self.get_butimg(button)
			self.texture_selection_buttons[button].config(image=self.texture_selection_button_images[button])
		if self.tex_name != "No texture selected":
			self.dispmod.config(imagefile=self.PROJECT.data[self.tex_name]["0file"])


	##########################################################################################################
	#PRE	:
	#POST	:
	def refresh_texture_list(self):
		print "refresh_texture_list() ran"
		self.listbox.delete(0, END)
		texlist = self.PROJECT.get_tex_list()
		for tex in texlist:
			self.listbox.insert(END, tex)
		if self.listbox.size() == 1 or (self.tex_name == "No texure selected" and self.listbox.size() > 1):
			self.listbox.selection_set(0)
			self.texture_onclick("null")
			#self.refresh_tex_conf()
		else:
			listofbox = self.listbox.get(0, END)
			key = 0
			for value in listofbox:
				if value == self.tex_name:
					self.listbox.selection_set(key)
					self.texture_onclick("null")
					#self.refresh_tex_conf()
				key += 1

	##########################################################################################################
	#PRE	:
	#POST	:
	def refresh_rottex_list(self):
		print "refresh_rottex_list() just ran"
		self.rotsellistbox.delete(0, END)
		if self.tex_name != "No texture selected":
			rottexlist = self.PROJECT.get_rottex_list(self.tex_name)
			for tex in rottexlist:
				self.rotsellistbox.insert(END, tex)

		if self.rotsellistbox.size() == 1 or (self.rot_name == "No rotation selected" and self.rotsellistbox.size() > 0):
			self.rotsellistbox.selection_set(0)
			self.tex_rotver_onclick("null")
			#self.refresh_offset_conf()
		else:
			listofbox = self.rotsellistbox.get(0, END)
			key = 0
			for value in listofbox:
				if value == self.rot_name:
					self.rotsellistbox.selection_set(key)
					self.tex_rotver_onclick("null")
					#self.refresh_offset_conf()
				key += 1

	##########################################################################################################
	#PRE	:
	#POST	:
	def refresh_tex_conf(self):
		print "refresh_tex_conf() just ran"
		if self.tex_name != "No texture selected":
			for key in self.PROJECT.data[self.tex_name]['rotated'].keys():
				self.rotspin[key]["var"].set(self.PROJECT.data[self.tex_name]['rotated'][key][0])
		if self.tex_list_sel == () or self.tex_name == "No texture selected":
			self.texture_configuration_frame.grid_forget()
		else:
			self.texture_configuration_frame.grid()
		self.texture_configuration_frame.config(text = self.tex_name)

		self.refresh_texture_buttons()
		self.refresh_rottex_list()
		self.refresh_offset_conf()

	##########################################################################################################
	#PRE	:.set ( value )
	#POST	:
	def refresh_offset_conf(self):
		print "refresh_offset_conf() ran"
		self.rotationdictionary = {"norot":0, "90cw":1, "180cw":2, "270cw":3, "xax":4, "yax":5}
		
		rotationflip = self.rotationdictionary[self.rot_name[:-3]]
		self.dispmod.config(offx=self.offsets[0], offy=self.offsets[1], scale=self.offsets[2], rotationflip=rotationflip)


#######################################################################################################################
####BUTTON CALLS#######################################################################################################
#######################################################################################################################

	##########################################################################################################
	#PRE	:
	#POST	:
	def modtexfilepath(self,button):
		print "modtexfilepath() ran"
		filename = askopenfilename(filetypes=[(".jpg files","*.jpg"),(".png files","*.png"),("allfiles","*")])
		if filename != "":
			self.PROJECT.set_tex_path(self.tex_name, button, filename)
		self.refresh_texture_buttons()

	##########################################################################################################
	#PRE	:
	#POST	:
	def blanktexfilepath(self,button):
		print "blanktexfilepath() ran"
		filename = ""
		self.PROJECT.set_tex_path(self.tex_name, button, filename)
		self.refresh_texture_buttons()
		self.refresh_tex_conf
			

#######################################################################################################################
####ONCLICKS###########################################################################################################	
#######################################################################################################################

	##########################################################################################################
	#PRE	:
	#POST	:
	def texture_onclick(self, event):
		print "texture_onclick() ran"
		previous_tex_list_sel = self.tex_list_sel
		self.tex_list_sel = self.listbox.curselection()
		if previous_tex_list_sel != self.tex_list_sel:
			if self.tex_list_sel != ():
				self.tex_name = self.listbox.get(self.tex_list_sel)
				self.refresh_tex_conf()
		if self.tex_list_sel == () or self.tex_name == "No texture selected":
			self.texture_configuration_frame.grid_forget()
		else:
			self.texture_configuration_frame.grid()
		self.texture_configuration_frame.config(text = self.tex_name)

	##########################################################################################################
	#PRE	:
	#POST	:
	def tex_rotver_onclick(self, event):
		print "tex_rotver_onclick ran"
		previous_rot_list_sel = self.rot_list_sel
		self.rot_list_sel = self.rotsellistbox.curselection()
		if previous_rot_list_sel != self.rot_list_sel:
			if self.rot_list_sel != ():
				self.rot_name = self.rotsellistbox.get(self.rot_list_sel)
				self.offsets = self.PROJECT.get_rot_prop(self.tex_name, self.rot_name)
		self.refresh_offset_conf()

	##########################################################################################################
	#PRE	:
	#POST	:
	def offset_conf_onclick(self, scaleval):
		print "offset_conf_onclick() ran"
		if self.rot_name != "No rotation selected":
			offsets = self.dispmod.get()
			self.offsets[0] = offsets[0]
			self.offsets[1] = offsets[1]
			self.offsets[2] = offsets[2]
			self.PROJECT.set_rot_prop(self.tex_name, self.rot_name, self.offsets)

	##########################################################################################################
	#PRE	:
	#POST	:
	def rot_spin_onclick(self):
		print "rot_spin_onclick ran"
		if self.tex_name != "No texture selected":
			for rotationkey in self.PROJECT.data[self.tex_name]['rotated'].keys():
				self.PROJECT.data[self.tex_name]['rotated'][rotationkey][0] = self.rotspin[rotationkey]["var"].get()
			if self.listbox.curselection() != ():
				self.tex_list_sel = self.listbox.curselection()
				self.tex_name = self.listbox.get(self.tex_list_sel)
			self.PROJECT.mend_rots(self.tex_name)
		self.refresh_tex_conf()
		self.refresh_rottex_list()


#######################################################################################################################
####RETURNS############################################################################################################	
#######################################################################################################################

	##########################################################################################################
	#PRE	:
	#POST	:
	def get_butimg(self, button):
		if self.tex_name != "No texture selected":
			teximgloc = self.PROJECT.data[self.tex_name][button]
		else:
			teximgloc = ""

		if teximgloc != "":
			retimgh = Image.open(teximgloc)
			retimgb = retimgh.resize((50, 50), Image.NEAREST)
			retimg = ImageTk.PhotoImage(retimgb)
		else:
			retimg = self.notexture
		return retimg

	##########################################################################################################
	#PRE	:
	#POST	:
	def tex_gen_prop(self):
		title_string = "Texture Properties | " + str(self.tex_name)
		texture_properties = Texconfigdialog(self.parent, title_string)
		if texture_properties.applied:
			return texture_properties.texturename
		else:
			return False

#######################################################################################################################
####MENU CALLS#########################################################################################################
#######################################################################################################################

	##########################################################################################################
	#PRE	:
	#POST	:
	def add_newtex(self):
		print "#######################################################################"
		tex_name = self.tex_gen_prop()
		if tex_name != "0none":
			tex_data = {
					"texname"	: tex_name,
					"0file"		: "",
					"dfile"		: "",
					"nfile"		: "",
					"sfile"		: "",
					"gfile"		: "",
					"zfile"		: "",
					"rotated"	: {"norot":[1,{"norot(1)":[0,0,1]}],"90cw":[0,{}],"180cw":[0,{}],"270cw":[0,{}],"xax":[0,{}],"yax":[0,{}]}
					}
			self.PROJECT.newtex(tex_name, tex_data)
			self.refresh_texture_list()

	##########################################################################################################
	#PRE	:
	#POST	:
	def removetex(self):
		if self.tex_name != "No texture selected":
			self.PROJECT.deltex(self.tex_name)
			self.initializecurrenttexvariables()
			self.tex_name = "No texture selected"
			self.refresh_texture_list()

	##########################################################################################################
	#PRE	:
	#POST	:
	def tex_prop_menu_item(self):
		if self.tex_name != "No texture selected":
			newname = self.tex_gen_prop()
			oldname = self.tex_name
			if newname != False:
				self.PROJECT.set_tex_name(oldname, newname)
				self.tex_name = newname
				self.refresh_texture_list()
				self.refresh_tex_conf()

	##########################################################################################################
	#PRE	:
	#POST	:	
	def new_project(self):
		del self.PROJECT
		self.PROJECT = Project()
		self.initializecurrenttexvariables()
		self.refresh_texture_list()
		self.refresh_tex_conf()

	##########################################################################################################
	#PRE	:
	#POST	:
	def open_project(self):
		filename =askopenfilename(filetypes=[("sbmcp files","*.sbmcp"),("allfiles","*")])
		if filename != "":
			self.PROJECT.popen(filename)
		self.refresh_texture_list()
		self.initializecurrenttexvariables()

	##########################################################################################################
	#PRE	:
	#POST	:
	def save_project(self):
		if self.PROJECT.projectfilename != "":
			self.PROJECT.psave()
		else:
			self.saveas_project()

	##########################################################################################################
	#PRE	:
	#POST	:			
	def properties_project(self):
		projectconfigwin = Project_conf_dialog(
			self.parent, 
			project_dir = self.PROJECT.get_tex_dir(),
			project_name = self.PROJECT.get_ptitle(),
			project_author = self.PROJECT.get_pauthor()
			)
		if projectconfigwin.applied:
			
			self.PROJECT.set_tex_dir(projectconfigwin.project_dir)
			self.PROJECT.set_ptitle(projectconfigwin.project_name)
			self.PROJECT.set_pauthor(projectconfigwin.project_author)
	##########################################################################################################
	#PRE	:
	#POST	:
	def exportcfg(self):
		cfgoutput = self.PROJECT.mkcfg()
		print "###########################################################################"
		for line in cfgoutput:
			print line,
		print "###########################################################################"

	##########################################################################################################
	#PRE	:
	#POST	:
	def generalconfig(self):
		genfigwin = Generalprogramconf(self.parent, "Preferences", CONFIG=CONFIG)
		if genfigwin.applied:
			CONFIG.setspath(genfigwin.cfg['sauerpath'])
	##########################################################################################################
	#PRE	:
	#POST	:
	def saveas_project(self):
		filename = asksaveasfilename(filetypes=[("sbmcp files","*.sbmcp"),("allfiles","*")])
		if filename != "":
			self.PROJECT.psetfile(filename)
			self.PROJECT.psave()

	##########################################################################################################
	#PRE	:
	#POST	:
	def about(self):
		aboutdialog = Aboutdialog(self.parent)


clear_screen()
global CONFIG
CONFIG = Config()
CONFIG.setos(os.name)

root = Tk()
app = App(root)
root.mainloop()

