import sys, cv2 as cv
import numpy as np

# load imagine
im = cv.imread(sys.argv[1], 1)

# binary imagine
gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
blur = cv.blur(gray, (3, 3))
ibin = cv.threshold(blur, 127, 255, cv.THRESH_OTSU)[1]
rows, cols = ibin.shape
res = cv.resize(ibin, None, fx = 780. / cols, fy = 220. / rows, interpolation = cv.INTER_CUBIC)
# cv.imshow("res", res)
# cv.waitKey()

# get matrix
field = [[0] * 780 for i in range(220)]
for i in range(780):
	for j in range(220):
		if res[j, i] == 0:
			field[j][i] = 1

# find 4 rectangles
rect1 = []
for i in range(10, 110 - 10):
	for j in range(10, 390 - 10):
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
for i in range(110 + 10, 220 - 10):
	for j in range(10, 390 - 10):
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
for i in range(10, 110 - 10):
	for j in range(390 + 10, 780 - 10):
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
for i in range(110 + 10, 220 - 10):
	for j in range(390 + 10, 780 - 10):
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

# perspective transformation
pts1 = np.float32([[rect1x, rect1y], [rect3x, rect3y], [rect2x, rect2y], [rect4x, rect4y]])
pts2 = np.float32([[0, 0], [780, 0],[0, 220], [780, 220]])
M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(res, M, (780, 220))
cv.imshow("dst", dst)
cv.waitKey()

# get matrix
fieldnew = [[0] * 780 for i in range(220)]
for i in range(780):
	for j in range(220):
		if dst[j, i] == 0:
			fieldnew[j][i] = 1

# find lines
lineshor = []
for k in range(10):
	maxcount = 0
	for i in range(20):
		counter = 0
		for j in range(780):
			counter += fieldnew[10 + 20 * k + i][j]
		if counter > maxcount:
			maxcount = counter
			maxline = 10 + 20 * k + i
	lineshor.append(maxline)
lineshor.append(220)
# print lineshor

linesvert = []
for k in range(8):
	maxcount = 0
	for j in range(180 + 75 * k - 35, 180 + 75 * k + 35):
		counter = 0
		for i in range(220):
			counter += fieldnew[i][j]
		if counter > maxcount:
			maxcount = counter
			maxline = j
	linesvert.append(maxline)
linesvert.append(780)
# print linesvert

# make massive with pluses (new)
massive = []
massive = [[" "] * 8 for i in range(10)]
for k in range(8):
	for l in range(10):
		counter = 0
		for i in range(3, lineshor[l + 1] - lineshor[l] - 3):
			for j in range(3, linesvert[k + 1] - linesvert[k] - 3):
				counter += fieldnew[lineshor[l] + i][linesvert[k] + j]
		if counter >= 1:
			massive[l][k] = "+"
		else:
			massive[l][k] = "-"
# for i in range(len(massive)):
# 	print massive[i]

# make file with pluses
with open('conduit.csv', 'w') as f_write:
	for i in range(8):
		f_write.write(" ".join(map(str, massive[i])) + '\n')

# # make massive with pluses
# massive = [[0] * 8 for i in range(10)]
# for k in range(8):
# 	for l in range(10):
# 		area = [[0] * 75 for i in range(20)]
# 		for i in range(75):
# 			for j in range(20):
# 				area[j][i] = fieldnew[20 + 20 * l + j][180 + 75 * k + i]
# 		counter = 0
# 		for i in range(4, 75 - 4):
# 			for j in range(4, 20 - 4):
# 				if area[j][i] == 1:
# 					counter += 1
# 		if counter >= 5:
# 			massive[l][k] = 1
# print " ".join(map(str, massive))
