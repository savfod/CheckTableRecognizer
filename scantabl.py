#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, cv2 as cv
import numpy as np
from math import *

# get quantity of students and tasks
if len(sys.argv)==5:
	image_file = sys.argv[1]
	groups_file = sys.argv[2]
	tasks = int(sys.argv[3])
	students = int(sys.argv[4])
else:
	print("usage: python "+sys.argv[0]+" imageFile groupsFile TaskCount StudentsCount")
	print("\nEXPECTED 4 PARAMS, " + str(len(sys.argv)-1) + " FOUND, USING EXAMPLE PARAMETERS:")
	image_file = "example/image.jpg"; print("imageFile = example/image.jpg")
	groups_file = "example/groups.txt"; print("groupsFile = example/groups.txt")
	tasks = 8; print("TaskCount = 8")
	students = 10; print("StudentsCount = 10")

COL_NAME_LENGTH = 180
COL_TASK_LENGTH = 75
REC_SIZE=1 #not only picture. Big value can affect on recognition
#BLACK_THRESHOLD=150

def calc_sizes():
	height = 20 * (students + 1)
	length = COL_NAME_LENGTH + COL_TASK_LENGTH * tasks
	return height, length

# load and binary imagine
def make_binary_image(cv, height, length):
	im = cv.imread(image_file, 1)
	gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
	blur = cv.blur(gray, (3, 3))
	rows, cols = blur.shape
	res = cv.resize(blur, None, fx = float(length) / cols, fy = float(height) / rows, interpolation = cv.INTER_CUBIC)
	ibin = cv.adaptiveThreshold(res, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 4)
	cv.imwrite('ibin.png', ibin)
	# cv.imshow('ibin.png', ibin)
	# cv.waitKey()

	# 
	# find best bin-threshold
	# ibin  = cv.threshold(res, BLACK_THRESHOLD, 255,  cv.THRESH_OTSU)[1]
	# cv.imwrite('ibin.png', ibin)
	# ibin1 = cv.threshold(res, BLACK_THRESHOLD, 255, cv.THRESH_BINARY)[1]
	# cv.imwrite('ibin1.png', ibin1)
	# ibin2 = cv.threshold(res, BLACK_THRESHOLD, 255, cv.THRESH_BINARY_INV)[1]
	# cv.imwrite('ibin2.png', ibin2)
	# ibin3 = cv.threshold(res, BLACK_THRESHOLD, 255, cv.THRESH_TRUNC)[1] 
	# cv.imwrite('ibin3.png', ibin3)
	# ibin4 = cv.threshold(res, BLACK_THRESHOLD, 255, cv.THRESH_TOZERO)[1]
	# cv.imwrite('ibin4.png', ibin4)
	# ibin5 = cv.threshold(res, BLACK_THRESHOLD, 255, cv.THRESH_TOZERO_INV)[1]
	# cv.imwrite('ibin5.png', ibin5)
	# ibin6 = cv.adaptiveThreshold(res, 255, cv.ADAPTIVE_THRESH_MEAN_C,  cv.THRESH_BINARY, 11, 2)
	# cv.imwrite('ibin6.png', ibin6)
	# ibin7 = cv.adaptiveThreshold(res, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
	# cv.imwrite('ibin7.png', ibin7)
	# ibin8 = cv.adaptiveThreshold(res, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 3) #
	# cv.imwrite('ibin8.png', ibin8)
	# ibin9 = cv.adaptiveThreshold(res, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 19, 4) #best
	# cv.imwrite('ibin9.png', ibin9)
	return ibin

# find 4 rectangles
def find_rectangles(field, height, length):
	rect1 = []
	for i in range(10, height // 2 - 10):
		for j in range(10, length // 2 - 10):
			counter = 0
			for l in range(9):
				for k in range(9):
					if field[i - l][j - k] == 1:
						counter += 1
					if field[i - l - 1][j + k + 1] == 0:
						counter += 1
					if field[i + l + 1][j - k - 1] == 0:
						counter += 1
			for l in range(4):
				for k in range(4):
					if field[i + l][j + k] == 1:
						counter += 1
			rect1.append([counter, j, i])

	maximum = 0
	for i in range(len(rect1)):
		if rect1[i][0] > maximum:
			maximum = rect1[i][0]
			rect1x = rect1[i][1]
			rect1y = rect1[i][2]

	rect2 = []
	for i in range(height // 2 + 10, height - 10):
		for j in range(10, length // 2 - 10):
			counter = 0
			for l in range(9):
				for k in range(9):
					if field[i + l][j - k] == 1:
						counter += 1
					if field[i - l - 1][j - k - 1] == 0:
						counter += 1
					if field[i + l + 1][j + k + 1] == 0:
						counter += 1
			for l in range(4):
				for k in range(4):
					if field[i - l][j + k] == 1:
						counter += 1
			rect2.append([counter, j, i])
	maximum = 0
	for i in range(len(rect1)):
		if rect2[i][0] > maximum:
			maximum = rect2[i][0]
			rect2x = rect2[i][1]
			rect2y = rect2[i][2]

	rect3 = []
	for i in range(10, height // 2 - 10):
		for j in range(length // 2 + 10, length - 10):
			counter = 0
			for l in range(9):
				for k in range(9):
					if field[i - l][j + k] == 1:
						counter += 1
					if field[i - l - 1][j - k - 1] == 0:
						counter += 1
					if field[i + l + 1][j + k + 1] == 0:
						counter += 1
			for l in range(4):
				for k in range(4):
					if field[i + l][j - k] == 1:
						counter += 1
			rect3.append([counter, j, i])
	maximum = 0
	for i in range(len(rect1)):
		if rect3[i][0] > maximum:
			maximum = rect3[i][0]
			rect3x = rect3[i][1]
			rect3y = rect3[i][2]

	rect4 = []
	for i in range(height // 2 + 10, height - 10):
		for j in range(length // 2 + 10, length - 10):
			counter = 0
			for l in range(9):
				for k in range(9):
					if field[i + l][j + k] == 1:
						counter += 1
					if field[i - l - 1][j + k + 1] == 0:
						counter += 1
					if field[i + l + 1][j - k - 1] == 0:
						counter += 1
			for l in range(4):
				for k in range(4):
					if field[i - l][j - k] == 1:
						counter += 1
			rect4.append([counter, j, i])
	maximum = 0
	for i in range(len(rect4)):
		if rect4[i][0] > maximum:
			maximum = rect4[i][0]
			rect4x = rect4[i][1]
			rect4y = rect4[i][2]

	# print rect1x, rect1y
	# print rect2x, rect2y
	# print rect3x, rect3y
	# print rect4x, rect4y
	cv.rectangle(ibin, (rect1x - REC_SIZE, rect1y - REC_SIZE), (rect1x + REC_SIZE, rect1y + REC_SIZE), (0, 250, 0), 3)
	cv.rectangle(ibin, (rect2x - REC_SIZE, rect2y - REC_SIZE), (rect2x + REC_SIZE, rect2y + REC_SIZE), (0, 250, 0), 3)
	cv.rectangle(ibin, (rect3x - REC_SIZE, rect3y - REC_SIZE), (rect3x + REC_SIZE, rect3y + REC_SIZE), (0, 250, 0), 3)
	cv.rectangle(ibin, (rect4x - REC_SIZE, rect4y - REC_SIZE), (rect4x + REC_SIZE, rect4y + REC_SIZE), (0, 250, 0), 3)
	# cv.imwrite('ibinwithrect.png', ibin)
	# cv.imshow('ibinwithrect.png', ibin)
	# cv.waitKey()
	return rect1x, rect1y, rect2x, rect2y, rect3x, rect3y, rect4x, rect4y


# perspective transformation
def make_perspective_transformation(coords, ibin, height, length):
	rect1x, rect1y, rect2x, rect2y, rect3x, rect3y, rect4x, rect4y = coords
	pts1 = np.float32([[rect1x, rect1y], [rect3x, rect3y], [rect2x, rect2y], [rect4x, rect4y]])
	pts2 = np.float32([[0, 0], [length, 0],[0, height], [length, height]])
	M = cv.getPerspectiveTransform(pts1, pts2)
	dst = cv.warpPerspective(ibin, M, (length, height))
	# cv.imwrite('persptrans.png', dst)
	# cv.imshow('persptrans.png', dst)
	# cv.waitKey()
	return dst

# get matrix
def get_matrix(dst, height, length):
	fieldnew = [[0] * length for i in range(height)]
	for i in range(length):
		for j in range(height):
			if dst[j, i] == 0:
				fieldnew[j][i] = 1
	return fieldnew

# find lines
def find_horizontal_lines(students, fieldnew, height, length):
	maxline = 0
	lineshor = []
	for k in range(students):
		maxcount = 0
		for i in range(20 + 20 * k - 5, 20 + 20 * k + 5):
			counter = 0
			for j in range(length):
				counter += fieldnew[i][j]
			if counter > maxcount:
				maxcount = counter
				maxline = i
		lineshor.append(maxline)
	lineshor.append(height)
	return lineshor
# for i in range(len(lineshor)):
# 	dst = cv.rectangle(dst, (0, lineshor[i] - 3), (3, lineshor[i]), (0, 250, 0), 3)
# print lineshor
def find_vertical_lines(tasks, fieldnew, height, length):
	maxline = 0
	linesvert = []
	for k in range(tasks):
		maxcount = 0
		for j in range(COL_NAME_LENGTH + COL_TASK_LENGTH * k - 10, COL_NAME_LENGTH + COL_TASK_LENGTH * k + 10):
			counter = 0
			for i in range(height):
				counter += fieldnew[i][j]
			if counter > maxcount:
				maxcount = counter
				maxline = j
		linesvert.append(maxline)
	linesvert.append(length)
	return linesvert
# for i in range(len(linesvert)):
# 	dst = cv.rectangle(dst, (linesvert[i] - 3, 0), (linesvert[i], 3), (0, 250, 0), 3)
# print linesvert
# cv.imwrite('dstwithlines.png', dst)
# cv.imshow('dstwithlines.png', dst)
# cv.waitKey()

# make massive with pluses
def make_massive_with_pluses(tasks, students, lineshor, linesvert, fieldnew):
	massive = []
	massive = [[" "] * tasks for i in range(students)]
	for k in range(tasks):
		for l in range(students):
			counter = 0
			for i in range(lineshor[l] + 4, lineshor[l + 1] - 4):
				for j in range(linesvert[k] + 4, linesvert[k + 1] - 4):
					counter += fieldnew[i][j]
			if counter >= 1:
				massive[l][k] = "+"
			else:
				massive[l][k] = "-"
	return massive
		# roi = dst[lineshor[l] : lineshor[l + 1], linesvert[k] : linesvert[k + 1]]
		# cv.imwrite(str("roi") + str(8 * l + k) + str(".png"), roi)
		# cv.waitKey()

# find out number of group
def find_out_group_index(fieldnew):
	verticals = []
	for j in range(5, 175):
		counter = 0
		for i in range(20):
			counter += fieldnew[i][j]
		if counter >= 6:
			verticals.append([counter, j])
	group_index = len(verticals)
	if group_index != 1:
		for i in range(len(verticals) - 1):
			if abs(verticals[i + 1][1] - verticals[i][1]) < 5:
				group_index -= 1
	return group_index


# make dictionary with surnames
def make_dictionary_with_surnames(group_index):
	surnames = []
	with open(groups_file, 'r') as f_read:
		for line in f_read:
			surnames.append(line.decode(encoding = "utf8"))
	groups = [0]
	for i in range(len(surnames)):
		if len(surnames[i]) == 2:
			groups.append(i)
	group = []
	if group_index == len(groups):
		for i in range(groups[group_index - 1] + 1, len(surnames) - 1):
			group.append(surnames[i][:-1])
		group.append(surnames[-1])
	else:
		for i in range(groups[group_index - 1] + 1, groups[group_index]):
			group.append(surnames[i][:-1])
	return group

# make file with pluses	
def make_file_with_pluses(tasks, students, group, massive, group_index):
	num = []
	for i in range(tasks):
		num.append(i + 1)

	#print (students, ",".join(s.encode('utf-8') for s in group), massive)
	with open('conduit.csv', 'w') as f_write:
		f_write.write(str(group_index) + ';' + ";".join(map(str, num)) + '\n')
		for i in range(students):
			if i < len(group):
				f_write.write(group[i].encode('utf8') + ';' + ";".join(map(str, massive[i])) + '\n')
			else:
				f_write.write('UNKNOWN;' + ";".join(map(str, massive[i])) + '\n')

height, length = calc_sizes()
ibin = make_binary_image(cv, height, length)
field = get_matrix(ibin, height, length)
coords = find_rectangles(field, height, length)
dst = make_perspective_transformation(coords, ibin, height, length)
fieldnew = get_matrix(dst, height, length)
lineshor = find_horizontal_lines(students, fieldnew, height, length)
linesvert = find_vertical_lines(tasks, fieldnew, height, length)
massive = make_massive_with_pluses(tasks, students, lineshor, linesvert, fieldnew)
group_index = find_out_group_index(fieldnew)
group = make_dictionary_with_surnames(group_index)
make_file_with_pluses(tasks, students, group, massive, group_index)