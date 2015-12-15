#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

COL_NAME_LENGTH = 180
COL_TASK_LENGTH = 75
ROW_HEIGHT = 20

# get quantity of students, tasks and number of group
def get_params():
	group_file_name = sys.argv[1] 
	tasks = ["был", "1а", "1б", "2а", "2б", "2в", "2г", "3а", "3б", "4а", "4б", "5а", "5б", "5в", "прин", "комм1", "комм2"] #TODO
	tasks = [t.decode('utf8') for t in tasks]

	groups = []
	newgroup = []
	with open(group_file_name, 'r') as f_read:
		for line in f_read:
			line = line.strip()
			if len(line) <= 2:
				groups.append(newgroup)
				newgroup = []
			else:
				newgroup.append(line.decode(encoding = "utf8"))
		groups.append(newgroup)
		groups = groups[1:]

	return tasks, groups 


# make table
def make_table(tasks, names, group_index):
	length = COL_NAME_LENGTH + COL_TASK_LENGTH * len(tasks)
	height = ROW_HEIGHT * (len(names) + 1)
	img = Image.new('RGB', (length + 40, height + 40), (255, 255, 255))
	imgDrawer = ImageDraw.Draw(img)
	imgDrawer.rectangle((20, 20, length + 20, height + 20), fill = "#FFFFFF", outline = "#000000")
	imgDrawer.rectangle((0, 0, 20, 20), fill = "#000000", outline = "#000000")
	imgDrawer.rectangle((length + 20, 0, length + 40, 20), fill = "#000000", outline = "#000000")
	imgDrawer.rectangle((0, height + 20, 20, height + 40), fill = "#000000", outline = "#000000")
	imgDrawer.rectangle((length + 20, height + 20, length + 40, height + 40), fill = "#000000", outline = "#000000")
	for i in range(200, length + 20, 75):
		imgDrawer.line((i, 20, i, height + 20), fill = "#000000", width = 1)
	for i in range(40, height + 20, 20):
		imgDrawer.line((20, i, length + 20, i), fill = "#000000", width = 1)
	for i, task in enumerate(tasks):
		imgDrawer.text((200 + 75 * i + 37, 25), task, font = ImageFont.truetype("DejaVuSans.ttf", 12), fill = "black")

	# draw lines for number of names
	for i in range(group_index):
		imgDrawer.line((20 + 180 // (group_index+1) * (i+1), 20, 20 + 180 // (group_index+1) * (i+1), 40), fill = "#000000", width = 1)

	# write names
	for i in range(len(names)):
		imgDrawer.text((30, 20 * (i+2) + 5), names[i], font = ImageFont.truetype("DejaVuSans.ttf", 10), fill = (0,0,0))

	# save image
	img.save(str(group_index) + '-' + str(len(tasks)) + str(".png"))

tasks, groups  = get_params()
for i, group in enumerate(groups):
	make_table(tasks, group, i) 
