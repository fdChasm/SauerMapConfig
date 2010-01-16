#standard classes
from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk
from copy import deepcopy
import cPickle, os, time, tkMessageBox, ConfigParser, string

#custom classes
import tkSimpleDialog
import tkDispModWidget
from tkImageSelectionButtonWithClear import tkImageSelectionButtonWithClear
import sauerConfigWrite


##########################################################################################################
class Config:
	def __init__(self):
		print "initialized config class"
		self.ConfigPath = "config.ini"
		self.ConfigDefault = {
			"General.sauerpath":		"",
			"General.os":				""
			}
		self.config = self.loadcfg(self.ConfigPath, self.ConfigDefault)
		
		
	def setos(self, os):
		self.config["General.os"] = os
		print "Config os variable set to:", os
	
	def setspath(self, spath):
		self.config["General.sauerpath"] = spath
		print "Config Sauerbraten path variable set to:", spath
		self.dump()

	def loadcfg(self, file, config={}):
		"""
		returns a dictionary with key's of the form
		<section>.<option> and the values 
		"""
		config = config.copy()
		cp = ConfigParser.ConfigParser()
		cp.read(file)
		for sec in cp.sections():
			name = string.lower(sec)
			for opt in cp.options(sec):
				config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
		return config

	def writecfg(self, filename, config):
		"""
		given a dictionary with key's of the form 'section.option: value'
		write() generates a list of unique section names
		creates sections based that list
		use config.set to add entries to each section
		"""
		cp = ConfigParser.ConfigParser()
		sections = set([k.split('.')[0] for k in config.keys()])
		map(cp.add_section, sections)
		for k,v in config.items():
			s, o = k.split('.')
			cp.set(s, o, v)
		f = open(filename, "w")
		cp.write(f)
		f.close()
		
	def dump(self):
		self.writecfg(self.ConfigPath, self.config)
##########################################################################################################
class Aboutdialog(tkSimpleDialog.Dialog):
	def body(self, master):

		self.maintext = Label(master, text="Sauerbraten Map configuration tool\nBy Chasm")
		self.maintext.grid(row=0)
		return self.maintext # initial focus

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = Frame(self)

		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.ok)

		box.pack()

	#
	# standard button semantics

	def apply(self):
		return
##########################################################################################################
class Texconfigdialog(tkSimpleDialog.Dialog):

	def body(self, master):
		self.texturename = "0none"

		Label(master, text="Texture name:").grid(row=0)
		
		self.default_name = StringVar(value="testname")
		
		
		self.e1 = Entry(master, textvariable=self.default_name)

		self.e1.grid(row=0, column=1)
		return self.e1 # initial focus

	def apply(self):
		self.applied = True
		self.texturename = self.default_name.get()
##########################################################################################################
class Generalprogramconf(tkSimpleDialog.Dialog):
	def body(self, master, **options):
		self.CONFIG = options['CONFIG']
		self.bodymaster = master
		if self.CONFIG.config["General.sauerpath"] == "":
			if self.CONFIG.config["General.os"] == "nt":
				self.directory = "C:/Program Files/Sauerbraten/"
			elif self.CONFIG.config["General.os"] == "posix":
				self.directory = "/usr/lib/games/sauerbraten/"
			else:
				self.directory = ""
		else:
			self.directory = self.CONFIG.config["General.sauerpath"]

		Label(master, text="Sauerbraten Installation Directory:").grid(row=0)
		self.sb_idir = StringVar(value=self.directory)
		self.sbidir = Entry(master, textvariable=self.sb_idir)
		self.sbidir.grid(row=1, column=0, sticky='nwes')


		self.bbrowse = Button(master, text="browse", command=self.browse_for_location)
		self.bbrowse.grid(row=1, column=1, sticky='nw')
		return self.sbidir # initial focus
	def buttonbox(self):
		# override the standard buttons
		box = Frame(self)

		w = Button(box, text="Apply", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def browse_for_location(self):
		sbidir = self.sb_idir.get()
		if os.path.exists(sbidir):
			initdir = self.sb_idir.get()
		else:
			initdir = os.path.expanduser("~/")
		dirname = askdirectory(parent=self.bodymaster,initialdir=initdir,title='Please select a directory')
		self.sbidir.delete(0, END)
		self.sbidir.insert(0, dirname)
	def apply(self):
		self.applied = True
		self.cfg = {}
		self.cfg['sauerpath'] = self.sb_idir.get()
##########################################################################################################
class Project_conf_dialog(tkSimpleDialog.Dialog):

	def body(self, master, **options):
		self.project_name = options['project_name']
		self.project_author = options['project_author']
		self.directory = options['project_dir']
		self.bodymaster = master
		
		Label(master, text="Project name:").grid(row=0)
		self.pj_name_var = StringVar(value=self.project_name)
		self.pj_name = Entry(master, textvariable=self.pj_name_var)
		self.pj_name.grid(row=1, column=0, sticky='nwes')		

		Label(master, text="Project author:").grid(row=2)
		self.pj_author_var = StringVar(value=self.project_author)
		self.pj_author = Entry(master, textvariable=self.pj_author_var)
		self.pj_author.grid(row=3, column=0, sticky='nwes')		
		
		Label(master, text="Project texture directory:").grid(row=4)
		self.pj_dir_var = StringVar(value=self.directory)
		self.pj_dir = Entry(master, textvariable=self.pj_dir_var)
		self.pj_dir.grid(row=5, column=0, sticky='nwes')


		self.bbrowse = Button(master, text="browse", command=self.browse_for_location)
		self.bbrowse.grid(row=5, column=1, sticky='nw')
		return self.pj_name # initial focus
	def buttonbox(self):
		# override the standard buttons
		box = Frame(self)

		w = Button(box, text="Apply", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def browse_for_location(self):
		sbidir = self.sb_idir.get()
		if os.path.exists(sbidir):
			initdir = self.sb_idir.get()
		else:
			initdir = os.path.expanduser("~/")
		dirname = askdirectory(parent=self.bodymaster,initialdir=initdir,title='Please select a directory')
		self.sbidir.delete(0, END)
		self.sbidir.insert(0, dirname)
	def apply(self):
		self.applied = True
		self.project_dir = self.pj_dir_var.get()
		self.project_name = self.pj_name_var.get()
		self.project_author = self.pj_author_var.get()
##########################################################################################################
class Project:
	def __init__(self):
		self.projectfilename = ""
		self.title = "untitled"
		self.author = "unknown"
		self.ctexdir = None
		self.data = {}
	def popen(self, filename):
		f = open(filename, 'r')
		filecontents = cPickle.load(f)
		f.close()
		self.title = filecontents["title"]
		self.author = filecontents["author"]
		self.ctexdir = filecontents["ctexdir"]
		self.data = filecontents["datatree"]
		self.projectfilename = filename
		print "Opened project:", self.projectfilename
	def get_tex_list(self):
		return_list = []
		for key in self.data.keys():
			return_list.append(key)
		return return_list
	def get_rottex_list(self, tex_name):
		return_list = []
		for key in self.data[tex_name]['rotated'].keys():
			if self.data[tex_name]['rotated'][key][0] > 0:
				for item in self.data[tex_name]['rotated'][key][1].keys():
					return_list.append(item)
		return return_list
	def mend_rots(self, tex_name):
		print "mend rots ran"
		for key in self.data[tex_name]['rotated'].keys():
			numberofrots = self.data[tex_name]['rotated'][key][0]
			curnumberofrots = len(self.data[tex_name]['rotated'][key][1].keys())
			
			if curnumberofrots > numberofrots:
				for rkey in self.data[tex_name]['rotated'][key][1].keys():
					rotnum = int(item_between_perentheses(rkey))
					if rotnum > numberofrots:
						del self.data[tex_name]['rotated'][key][1][rkey]
			elif curnumberofrots < numberofrots:
				#add the missing indexes and blank coordinate list
				while len(self.data[tex_name]['rotated'][key][1]) < numberofrots:
					namestring = key + "(" + str((len(self.data[tex_name]['rotated'][key][1])+1)) + ")"
					self.data[tex_name]['rotated'][key][1][namestring] = [0,0,1]
					curnumberofrots = len(self.data[tex_name]['rotated'][key][1].keys())
	def get_rot_prop(self, tex_name, rot_name):
		rottype = rot_name[:(len(rot_name)-3)]
		retitem = self.data[tex_name]['rotated'][rottype][1][rot_name]
		return retitem
	def set_rot_prop(self, tex_name, rot_name, rotprop):
		rottype = rot_name[:(len(rot_name)-3)]
		self.data[tex_name]['rotated'][rottype][1][rot_name] = rotprop
	def set_tex_name(self, oldtex_name, newtex_name):
		self.data[newtex_name] = deepcopy(self.data[oldtex_name])
		del self.data[oldtex_name]
	def set_tex_prop(self, tex_name, tex_data):
		self.data[tex_name] = tex_data
	def set_tex_path(self, tex_name, tex_type, path):
		self.data[tex_name][tex_type] = path
	def get_tex_prop(self, tex_name):
		return self.data[tex_name]
	def deltex(self, tex_name):
		del self.data[tex_name]
	def newtex(self, tex_name, tex_data):
		self.data[tex_name] = deepcopy(tex_data)
	def psetfile(self, filename):
		self.projectfilename = filename
	def psave(self):
		dumpcontents = {}
		dumpcontents["title"] = self.title
		dumpcontents["author"] = self.author
		dumpcontents["ctexdir"] = self.ctexdir
		dumpcontents["datatree"] = self.data
		f = open(self.projectfilename, 'w')
		cPickle.dump(dumpcontents, f)
		f.close()
		print "Project saved as:", self.projectfilename
	def get_ptitle(self):
		return self.title
	def set_ptitle(self, title):
		self.title = title
	def get_pauthor(self):
		return self.author
	def set_pauthor(self, author):
		self.author = author
	def get_tex_dir(self):
		return self.ctexdir
	def set_tex_dir(self, directory):
		self.ctexdir = directory
	def mkcfg(self):
		dumpcontents = {}
		dumpcontents["title"] = self.title
		dumpcontents["author"] = self.author
		dumpcontents["ctexdir"] = self.ctexdir
		dumpcontents["datatree"] = self.data
		returnlist = sauerConfigWrite.configwrite(dumpcontents)
		return returnlist