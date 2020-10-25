"""
screenStitch.py

Will ask for files, find the region that changed between first two files,
crop the changes, and stitch a final image together.

Outputs a new stitch.png in the directory of first selected image and will
overwrite any existing files with same name.

By jaflo at github: https://github.com/jaflo/screenStitch/
Licensed under the MIT license (http://opensource.org/licenses/MIT)

If you make any changes or use this in a project, I would appreciate
if you tell me. Please leave this notice intact.
"""

from PIL import Image, ImageChops
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import subprocess
import platform
import shutil
import os

if platform.system()=="Windows":
	foldersep = "\\"
else:
	foldersep = "/"
Tk().withdraw()
files = askopenfilenames(title="Choose images")
print("Choose images to compare")
images = []
i = 0
imagergbprev = 0
leftmost = 1e9
rightmost = 0
topmost = 1e9
bottommost = 0

if not os.path.exists("stitchtmp"):
    os.makedirs("stitchtmp")

for file in files:
	image = Image.open(file)
	imagergb = image.convert("RGB")
	if i == 1:
		print("Performing analysis")
		width, height = image.size
		for x in range(1, width):
			for y in range(1, height):
				r, g, b = imagergb.getpixel((x, y))
				if imagergb.getpixel((x, y)) != imagergbprev.getpixel((x, y)):
					#print("%d, %d" % (x, y))
					if leftmost > x:
						leftmost = x
					if rightmost < x:
						rightmost = x
					if topmost > y:
						topmost = y
					if bottommost < y:
						bottommost = y
		print("Differences at (%d, %d) to (%d, %d)" % (leftmost, rightmost, topmost, bottommost))
	if i > 0:
		if i == 1:
			imagergbprev.crop((leftmost, topmost, rightmost, bottommost)).save("stitchtmp"+foldersep+"diff0.png")
		else:
			imagergbprev.crop((leftmost, topmost, rightmost, bottommost)).save("stitchtmp"+foldersep+"diff"+str(i-1)+".png")
		if i == (len(files)-1):
			imagergb.crop((leftmost, topmost, rightmost, bottommost)).save("stitchtmp"+foldersep+"diff"+str(i)+".png")
	imagergbprev = imagergb
	i+=1

total = i + 1
i = 0
fullimage = Image.new("RGB", (rightmost-leftmost-11, 9999), "black")
Image.new("RGB", (rightmost-leftmost, 2000), "black").save("stitchtmp"+foldersep+"diff"+str(total-1)+".png")
lineonnew = 0

print("Stitching")
for num in range(0, total):
	if i > 0:
		image1 = Image.open("stitchtmp"+foldersep+"diff"+str(i-1)+".png")
		image2 = Image.open("stitchtmp"+foldersep+"diff"+str(i)+".png")
		image1rgb = image1.convert("RGB")
		image2rgb = image2.convert("RGB")
		width, height = image1.size
		sodone = False
		for line in range(0, height):
			im1 = image1rgb.crop((0, line, width, line+1))
			im2 = image2rgb.crop((0, 1, width, 2))
			if ImageChops.difference(im1, im2).getbbox() is None:
				sodone = True
			else:
				if not sodone:
					fullimage.paste(im1, (0,lineonnew))
					lineonnew+=1
	i+=1

print("Cropping")
bg = Image.new(fullimage.mode, fullimage.size, (0,0,0))
diff = ImageChops.difference(fullimage, bg)
diff = ImageChops.add(diff, diff, 2.0, -100)
bbox = diff.getbbox()
if bbox:
	fullimage = fullimage.crop(bbox)

if platform.system()=="Windows":
	fullimage.save(files[0][0:files[0].rfind(foldersep)]+foldersep+"stitch.png")
	subprocess.Popen(r'explorer /select,"'+files[0][0:files[0].rfind(foldersep)]+foldersep+'stitch.png"')
else:
	fullimage.save(files[0][0:files[0].rfind(foldersep)]+foldersep+"stitch.png")
	if platform.system()=="Darwin":
		subprocess.call(["open", "-R", files[0][0:files[0].rfind(foldersep)]+foldersep+"stitch.png"])

shutil.rmtree("stitchtmp")
print("Done!")
