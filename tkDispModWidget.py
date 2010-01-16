from Tkinter import *
from PIL import Image, ImageTk, ImageChops, ImageOps

class tkDispModWidget(Frame):
	class ImageSoi:
		def __init__(self):
			self.imagefile = 'notexture.jpg'
			self.rotationflip = 0
			self.offx = 0
			self.offy = 0
			self.scale = float()
			self.scale = 1
			self.recalcimage()

		def recalcimage(self):
			self.image = Image.open(self.imagefile)
			
			self.image = self.applyflip(self.image)
			
			bbox = self.image.getbbox()
			scalex = int(bbox[2] * self.scale)
			scaley = int(bbox[3] * self.scale)
			self.image = self.image.resize((scalex, scaley), Image.BICUBIC)
			self.image = ImageChops.offset(self.image, self.offx, self.offy)
			bbox = self.image.getbbox()
			croptuple = (0, bbox[3] - 64, 64, bbox[2])
			self.image = self.image.crop(croptuple)
			self.image = self.image.resize((100, 100), Image.BICUBIC)
			self.image = ImageTk.PhotoImage(self.image)
			
		def applyflip(self, image):
			if self.rotationflip == 0:
				return image
			elif self.rotationflip == 1:
				return image.rotate(90)
			elif self.rotationflip == 2:
				return image.rotate(180)
			elif self.rotationflip == 3:
				return image.rotate(270)
			elif self.rotationflip == 4:
				return ImageOps.mirror(image)
			elif self.rotationflip == 5:
				return ImageOps.flip(image)

		def set(self, **options):
			if "imagefile" in options.keys():
				self.imagefile = options["imagefile"]
			if "rotationflip" in options.keys():
				self.rotationflip = options["rotationflip"]
			if "offx" in options.keys():
				self.offx = options["offx"]
			if "offy" in options.keys():
				self.offy = options["offy"]
			if "scale" in options.keys():
				self.scale = options["scale"]
			if options != {}:
				self.recalcimage()

	def __init__(self, parent, **options):
		Frame.__init__(self, parent, options)
		self.imagefile = 'notexture.jpg'
		self.rotationflip = 0
		self.draw_widget()

	def draw_widget(self):
		self.displaceframe = Frame(self, width = 144, borderwidth=1)
		self.rotdispframe = Frame(self.displaceframe, width = 80, height = 80)
		self.dispmodcanv = Canvas(self.rotdispframe, height = 100, width = 100)

		self.image = self.ImageSoi()

		self.dispmodimg = self.dispmodcanv.create_image( 0, 0, image=self.image.image, anchor=NW)

		self.dispmodcanv.grid(row = 1, column = 2,columnspan=1, sticky = 'snew')
		self.scalex = Scale(self.rotdispframe, orient=HORIZONTAL, showvalue = 0, from_=0, to=64, command=self.onmodcommand)
		self.scalex.grid(row = 2, column = 2, sticky = 'snew')
		self.scaley = Scale(self.rotdispframe, orient=VERTICAL, showvalue = 0, from_=64, to=0, command=self.onmodcommand)
		self.scaley.grid(row = 1, column = 1, sticky = 'snew')
		self.scalet = Scale(self.rotdispframe, orient=VERTICAL, showvalue = 1, from_=4, to=0.05, resolution=.05, command=self.onmodcommand)
		self.scalet.set(1)
		self.scalet.grid(row = 1, column = 3, rowspan= 2, sticky = 'wens')
		self.rotdispframe.grid(row = 2, column = 1, sticky = 'snew')
		self.displaceframe.pack()


	def onmodcommand(self, value):
		self.image.set(imagefile=self.imagefile, offx=self.scalex.get(), offy=self.scaley.get(), scale=self.scalet.get(), rotationflip=self.rotationflip)
		self.dispmodcanv.itemconfig(self.dispmodimg, image=self.image.image)
		self.command()

	def config(self, **options):
		if "command" in options.keys():
			self.command = options["command"]
		if "imagefile" in options.keys():
			self.imagefile = options["imagefile"]
			if options["imagefile"] == "":
				self.imagefile = 'notexture.jpg'
		if "rotationflip" in options.keys():
			self.rotationflip = options["rotationflip"]
		if "offx" in options.keys():
			self.scalex.set(options["offx"])
		if "offy" in options.keys():
			self.scaley.set(options["offy"])
		if "scale" in options.keys():
			self.scalet.set(options["scale"])
		if options != {}:
			self.onmodcommand(0)

	def get(self):
		offx=self.scalex.get()
		offy=self.scaley.get()
		scale=self.scalet.get()
		return (offx, offy, scale)


#class App:
#
#    def __init__(self, master):
#
#        frame = Frame(master)
#        frame.pack()
#
#        f = tkDispModWidget(frame)
#	f.config(test="Blah", var1="bulge")
#	f.pack()
#
#root = Tk()
#
#app = App(root)

#root.mainloop()


