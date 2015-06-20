#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, cv2 as cv
import numpy as np
from math import *

# get quantity of students and tasks
tasks = int(input())
students = int(input())
length = 180 + 75 * tasks
height = 20 * (students + 1)

# load imagine
im = cv.imread(sys.argv[1], 1)

# binary imagine
gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
blur = cv.blur(gray, (3, 3))
rows, cols = blur.shape
res = cv.resize(blur, None, fx = float(length) / cols, fy = float(height) / rows, interpolation = cv.INTER_CUBIC)
ibin = cv.threshold(res, 127, 255, cv.THRESH_OTSU)[1]
# cv.imwrite('ibin.png', ibin)
# cv.imshow('ibin.png', ibin)
# cv.waitKey()

# get matrix
field = [[0] * length for i in range(height)]
for i in range(length):
	for j in range(height):
		if ibin[j, i] == 0:
			field[j][i] = 1

# find 4 rectangles
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
# ibin = cv.rectangle(ibin, (rect1x - 2, rect1y - 2), (rect1x + 2, rect1y + 2), (0, 250, 0), 3)
# ibin = cv.rectangle(ibin, (rect2x - 2, rect2y - 2), (rect2x + 2, rect2y + 2), (0, 250, 0), 3)
# ibin = cv.rectangle(ibin, (rect3x - 2, rect3y - 2), (rect3x + 2, rect3y + 2), (0, 250, 0), 3)
# ibin = cv.rectangle(ibin, (rect4x - 2, rect4y - 2), (rect4x + 2, rect4y + 2), (0, 250, 0), 3)
# cv.imwrite('ibinwithrect.png', ibin)
# cv.imshow('ibinwithrect.png', ibin)
# cv.waitKey()

# perspective transformation
pts1 = np.float32([[rect1x, rect1y], [rect3x, rect3y], [rect2x, rect2y], [rect4x, rect4y]])
pts2 = np.float32([[0, 0], [length, 0],[0, height], [length, height]])
M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(ibin, M, (length, height))
# cv.imwrite('persptrans.png', dst)
# cv.imshow('persptrans.png', dst)
# cv.waitKey()

# get matrix
fieldnew = [[0] * length for i in range(height)]
for i in range(length):
	for j in range(height):
		if dst[j, i] == 0:
			fieldnew[j][i] = 1

# find lines
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
# for i in range(len(lineshor)):
# 	dst = cv.rectangle(dst, (0, lineshor[i] - 3), (3, lineshor[i]), (0, 250, 0), 3)
# print lineshor

linesvert = []
for k in range(tasks):
	maxcount = 0
	for j in range(180 + 75 * k - 10, 180 + 75 * k + 10):
		counter = 0
		for i in range(height):
			counter += fieldnew[i][j]
		if counter > maxcount:
			maxcount = counter
			maxline = j
	linesvert.append(maxline)
linesvert.append(length)
# for i in range(len(linesvert)):
# 	dst = cv.rectangle(dst, (linesvert[i] - 3, 0), (linesvert[i], 3), (0, 250, 0), 3)
# print linesvert
# cv.imwrite('dstwithlines.png', dst)
# cv.imshow('dstwithlines.png', dst)
# cv.waitKey()

# make massive with pluses
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
		# roi = dst[lineshor[l] : lineshor[l + 1], linesvert[k] : linesvert[k + 1]]
		# cv.imwrite(str("roi") + str(8 * l + k) + str(".png"), roi)
		# cv.waitKey()

# find out number of group
verticals = []
for j in range(5, 175):
	counter = 0
	for i in range(20):
		counter += fieldnew[i][j]
	if counter >= 6:
		verticals.append([counter, j])
number = len(verticals)
if number != 1:
	for i in range(len(verticals) - 1):
		if abs(verticals[i + 1][1] - verticals[i][1]) < 5:
			number -= 1

# make dictionary with surnames
surnames = []
with open('groups.txt', 'r') as f_read:
	for line in f_read:
		surnames.append(line.decode(encoding = "utf8"))
groups = [0]
for i in range(len(surnames)):
	if len(surnames[i]) == 2:
		groups.append(i)
group = []
if number == len(groups):
	for i in range(groups[number - 1] + 1, len(surnames) - 1):
		group.append(surnames[i][:-1])
	group.append(surnames[-1])
else:
	for i in range(groups[number - 1] + 1, groups[number]):
		group.append(surnames[i][:-1])

# make file with pluses	
with open('conduit.csv', 'w') as f_write:
	f_write.write(str(number) + ';1;2;3;4;5;6;7;8' + '\n')
	for i in range(students):
		f_write.write(group[i].encode('cp1251') + ';' + ";".join(map(str, massive[i])) + '\n')
