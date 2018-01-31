from music21 import *

# environment.set('musicxmlPath', '/usr/bin/musescore')
# environment.set('graphicsPath', '/usr/bin/convert')
# environment.set('midiPath', '/usr/bin/timidity')

def parseToDict(filepath, saveMuse=False):
	dict = {}
	s = converter.parse(filepath)
	measureMap = s.measureOffsetMap()
	offsets = list(measureMap.keys())
	offsets.sort()

	first_ms = measureMap[offsets[0]][0]
	# key
	dict['keySignature'] = first_ms.keySignature.sharps

	# time signature
	dict['timeSignature'] = (first_ms.timeSignature.numerator, first_ms.timeSignature.denominator)
	# print(dict['timeSignature'])
	# offset of first note
	dict['firstNoteOffset'] = offsets[0]

	# notes and rests
	dict['notesAndRests'] = []
	dict['notesAndRestsDurations'] = []
	if saveMuse:
		dict['NR4use'] = []

	for n in s.flat.notesAndRests:
		if isinstance(n, note.Rest):
			dict['notesAndRests'].append('R')
		elif isinstance(n, chord.Chord):
			# if chords are encountered, only record the root
			dict['notesAndRests'].append(n.pitchNames[0])
		else:
			dict['notesAndRests'].append(n.pitch.name + str(n.pitch.octave))
		# print(n.duration.quarterLength)
		dict['notesAndRestsDurations'].append(n.duration.quarterLength)
		if saveMuse:
			dict['NR4use'].append(n)
	# print(dict)
	return dict


def getNotesInArray(dict, minIntval=0.25):


	durations = dict['notesAndRestsDurations']
	notes = dict['notesAndRests']

	notesInArray = []
	skipped = 0
	#############################3
	# based on note length
	#############################

	possed = False
	trinote = 2
	for i, note in enumerate(notes):
		dur = durations[i]
		length = int(dur/minIntval)
		# print(int(dur/minIntval))
		if length >= 1:
			notesInArray.append(note)
			for i in range(length-1):
				notesInArray.append('_')
			possed = False
		elif dur/minIntval == 0.5:
			if possed == True:
				possed = False
			else:
				notesInArray.append(note)
				possed = True
		# elif dur/minIntval == 2/3.:
		# 	# irregular data, should skip anyway
		# 	if trinote == 2:
		# 		notesInArray.append(note)
		# 		trinote -= 1
		# 	elif trinote == 1:
		# 		# do not record
		# 		trinote -= 1
		# 		continue
		# 	elif trinote == 0:
		# 		notesInArray.append(note)
		# 		trinote = 2
		else:
			skipped += 1

	###############################
	# based on the length of clock
	###############################
	# clk = 0
	# tot_len = 0
	# is_filled = False
	# tmp_dur = 0
	# tmp_notes = []
	# for i, note in enumerate(notes):
		
	# 	dur = durations[i]/minIntval
	# 	# print(tot_len, clk)
		
	# 	length = int(dur)
	# 	if length >= 1:
	# 		notesInArray.append(note)
	# 		for i in range(length-1):
	# 			notesInArray.append('_')
	# 			clk += dur
	# 			tot_len += dur

	# 	else:
	# 		tmp_dur += dur
	# 		tmp_notes.append(note)
	# 		tmp_int = tmp_dur % 1
	# 		if tmp_int <= 0.001:
	# 			# it's a whole length
	# 			rest_len = tmp_int - 1
	# 			clk += tmp_int
	# 			notesInArray.append(note)
	# 			if rest_len > 0:
	# 				for i in range(round(rest_len)):
	# 					notesInArray.append('R')


	# print(skipped)
	# print(notesInArray)

	return notesInArray, skipped


def transformArrayToMuse(notesInArray, minIntval=0.25, saveMidi=False):
	dur = 1
	s = stream.Score()
	
	note_ = []
	offset = 0
	# tmp_note = 'C'
	for i, n in enumerate(notesInArray):

		note_.append(n)
		if n != '_' and i != 0:
			# compile to a muse note 
			dur = len(note_)-1
			# print(note_, dur*0.25)
			if note_[0] == 'R':
				# print(i)
				# rest
				nn = note.Rest()
				nn.duration.quarterLength = dur * minIntval
				s.insert(offset, nn)
				offset += dur * minIntval
				# s.append(note.Rest())
			else:
				# print(i, note_)
				nn = note.Note(note_[0])
				nn.duration.quarterLength = dur * minIntval
				s.insert(offset, nn)
				offset += dur * minIntval

			
			note_ = [n]

	if note_[0] == 'R':
		# rest
		nn = note.Rest()
		nn.duration.quarterLength = dur * minIntval
		s.insert(offset, nn)
		offset += dur * minIntval
		# s.append(note.Rest())
	else:
		nn = note.Note(note_[0])
		nn.duration.quarterLength = dur * minIntval
		s.insert(offset, nn)
		offset += dur * minIntval


	if saveMidi == True:
		mf = midi.translate.streamToMidiFile(s)
		mf.open('./midi.mid', 'wb')
		mf.write()
		mf.close()

	return s

def sanityLengthCheck(scores):
	t = []
	for s in scores:
		# t.append(s.highestTime)
		t.append(len(s))
	return t
if __name__ == "__main__":
	path = "/home/zhaocheng/Research/Kaggle/AIMusic/data/c3/3/02.md"
	dict = parseToDict(path)

	notesInArray, _ = getNotesInArray(dict)
	print(len(notesInArray))

	s = transformArrayToMuse(notesInArray)
	time = sanityLengthCheck([s])
	print(time)
