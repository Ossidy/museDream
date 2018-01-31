import os
from parse import *
import json

path = './data'

# rename all file
# for fn in os.listdir(path):
# 	for f2 in os.listdir(path+'/' +fn):
# 		all_data = []
# 		for f3 in os.listdir(path + '/' + fn + '/' + f2):
# 			print(f3+'.md')
# 			os.rename(path + '/' + fn + '/' + f2 + '/' + f3, path + '/' + fn + '/' + f2 + '/' + f3 + '.md')
			# if f3 in ['01','02','03','04','05']:
			# 	parseToDict(path + '/' + fn + '/' + f3 +'.md')


# parse all data into dictionary 
# path = './data'
# all_data = {}
# count = 0
# for fn in os.listdir(path):
# 	for f2 in os.listdir(path+'/' +fn):
# 		chapter = {}
# 		count += 1
# 		for f3 in os.listdir(path + '/' + fn + '/' + f2):
# 			print(f3)
# 			if f3 in ['01.md','02.md','03.md','04.md','05.md']:
# 				dict = parseToDict(path + '/' + fn + '/' + f2 + '/' + f3)
# 				chapter[f3[:2]] = dict
# 		all_data[fn+'_'+f2] = chapter

# print(len(all_data))
# with open('./data.txt', 'w') as outfile:
#     json.dump(all_data, outfile)


filename = './data.txt'
with open(filename, 'r') as f:
	data = json.load(f)

# print(data.keys())
# # print(data[0])
# for k in data:
# 	if len(data[k]) < 5:
# 		print(k, "not usable")
# 	else:
# 		for i in data['c1_1']:
# 			# print(k, i)
# 			# print(data[0][i])
# 			_, skippled = getNotesInArray(data[k][i])
# 			if skippled > 0:
# 				print(k, "multiple track", skippled)



# sanity check
usable = []
for k in data:
	if len(data[k]) < 5:
		print(k, "not usable")
	else:
		sp = 0
		# print(k)
		scores = []
		for i in data['c1_1']:
			# print(i)
			# print(k, i)
			# print(data[0][i])
			s, skipped = getNotesInArray(data[k][i])
			# print(s)
			if skipped > 0:
				sp = 1
				continue
			scores.append(s)
		# print(scores)
		if sp == 0:
			t = sanityLengthCheck(scores)
			print(k, t)
			if len(set(t)) == 1:
				# all tracks have same length
				usable.append(k)

print(usable)
for k in usable:
	length = len(getNotesInArray(data[k]['01'])[0])
	# length = len(nts)
	print(length)
