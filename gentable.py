#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# make table
img = Image.new('RGB', (820, 260), (255, 255, 255))
imgDrawer = ImageDraw.Draw(img)
imgDrawer.rectangle((20, 20, 800, 240), fill = "#FFFFFF", outline = "#000000")
imgDrawer.rectangle((0, 0, 20, 20), fill = "#000000", outline = "#000000")
imgDrawer.rectangle((800, 0, 820, 20), fill = "#000000", outline = "#000000")
imgDrawer.rectangle((0, 240, 20, 260), fill = "#000000", outline = "#000000")
imgDrawer.rectangle((800, 240, 820, 260), fill = "#000000", outline = "#000000")
for i in range(200, 800, 75):
	imgDrawer.line((i, 20, i, 240), fill = "#000000", width = 1)
for i in range(40, 240, 20):
	imgDrawer.line((20, i, 800, i), fill = "#000000", width = 1)
for i in range(8):
	imgDrawer.text((200 + 75 * i + 37, 25), str(i + 1), fill = "black")

# draw lines for number of group
number = int(input())
for i in range(number):
	imgDrawer.line((20 + 180 // (number + 1) * (i + 1), 20, 20 + 180 // (number + 1) * (i + 1), 40), fill = "#000000", width = 1)

# write names
surnames = []
with open('groups.txt', 'r') as f_read:
	for line in f_read:
		line.decode('cp1251')
		line = unicode(line, 'cp866')
		surnames.append(line[:-1])
for i in range(10):
	imgDrawer.text((30, 20 * (i + 2) + 5), surnames[11 * (number - 1) + i + 1], font = ImageFont.truetype("DejaVuSans.ttf", 12), fill = (0,0,0))

# save image
img.save("pil-example.png")
