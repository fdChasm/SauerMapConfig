from Tkinter import *
from PIL import Image, ImageTk, ImageChops

class tkImageSelectionButtonWithClear(Frame):
	def __init__(self, parent, **options):
		self.framekeys = ['bd', 'borderwidth', 'class', 'relief', 'background', 'bg', 'colormap', 'container', 'cursor', 'height', 'highlightbackground', 'highlightcolor', 'highlightthickness', 'padx', 'pady', 'takefocus', 'visual', 'width']
		frameoptions = {}
		self.otheroptions = {}
		for item in options.keys():
			if item in self.framekeys:
				frameoptions[item] = options[item]
			else:
				self.otheroptions[item] = options[item]

		if "command" in self.otheroptions.keys():
			self.command = self.otheroptions["command"]
		else:
			command = lambda: self.actnull()
			self.command = command
		if "xcommand" in self.otheroptions.keys():
			self.xcommand = self.otheroptions["xcommand"]
		else:
			xcommand = lambda: self.actnull()
			self.xcommand = xcommand
		if "image" in self.otheroptions.keys():
			self.image = self.otheroptions["image"]
		else:
			self.notexturehandle = Image.open("notexture.png")
			self.notex = self.notexturehandle.resize((40, 40), Image.BICUBIC)
			self.notexture = ImageTk.PhotoImage(self.notex)
			self.image = self.notexture
		if "text" in self.otheroptions.keys():
			self.buttontxt = self.otheroptions["text"]
		else:
			self.buttontxt = "defaulttxt"
		Frame.__init__(self, parent, **frameoptions)
		self.draw_widget()

	def draw_widget(self):
		self.frame = Frame(self)
		self.mainbutton = Button(self.frame, text=self.buttontxt, image=self.image, compound=TOP, command=self.mcallback, height = 64, width = 64)
		self.mainbutton.pack()
		self.xbutton = Button(self.frame, text="x", command=self.xcallback)
		self.frame.bind("<Enter>", self.packxbutton)
		self.frame.bind("<Leave>", self.unpackxbutton)
		self.frame.pack()

	def mcallback(self):
		self.command()

	def xcallback(self):
		self.xcommand()

	def actnull(self):
		return

	
	def packxbutton(self, mouse):
		if self.image != self.notexture:
			self.xbutton.place(in_=self.mainbutton, x=53, y=0)

	def unpackxbutton(self, mouse):
		self.xbutton.place_forget()

	def onmodcommand(self, value):
		self.mainbutton.config(text=self.buttontxt, image=self.image)

	def config(self, **options):
		frameoptions = {}
		self.otheroptions = {}
		for item in options.keys():
			if item in self.framekeys:
				frameoptions[item] = options[item]
			else:
				self.otheroptions[item] = options[item]
		#self.config(**frameoptions)

		if "command" in self.otheroptions.keys():
			self.command = self.otheroptions["command"]
		if "xcommand" in self.otheroptions.keys():
			self.xcommand = self.otheroptions["xcommand"]		
		if "image" in self.otheroptions.keys():
			self.image = self.otheroptions["image"]
		if "text" in self.otheroptions.keys():
			self.buttontxt = self.otheroptions["text"]
		if self.otheroptions != {}:
			self.onmodcommand(0)

#class App:
#
#	def __init__(self, master):
#
#		frame = Frame(master)
#		frame.pack()
#
#		f = tkImageSelectionButtonWithClear(frame, text="sometext", blah="garg")
#		#f.config(test="Blah", var1="bulge")
#		f.pack()
#
#root = Tk()
#
#app = App(root)
#
#root.mainloop()

