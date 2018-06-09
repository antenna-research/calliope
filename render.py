import music21 as m21
from utils import *
from pprint import pprint
from copy import copy, deepcopy

class Renderer(object):
	""" turns feature spellout into score object, with processing """

	def render(self, passage):
		part = m21.stream.Part()
		# cl = instrument.Clarinet()
		# p.insert(0, cl)

		for barDuration in passage.bars:
			m = m21.stream.Measure()
			m.timeSignature = deepcopy(timeSignatures[barDuration])
			part.append(m)
		measures = part.getElementsByClass('Measure')

		incrementPairs = [[passage.anacruses[i], passage.stations[i]] for i in range(len(passage.stations)) ]
		increments = []
		for pair in incrementPairs:
			increments.extend(pair)

		# split each lexeme in anacrusis and station, put them in a flat list
		splitLexemes = []
		for i, lexeme in enumerate(passage.spelling):
			pickup = {
				'_label': lexeme.label,
				'_offsets': [offset for offset in lexeme.realization['feet'][0] if offset < 0],
				'_nextOffset': firstNonNegative(lexeme.realization['feet'][0]), # 0
				'_duration': incrementPairs[i][0],
				'parent': lexeme,
			}
			station = {
				'_label': lexeme.label,
				'_offsets': [offset for offset in lexeme.realization['feet'][0] if offset >= 0],
				'_priorOffset': 0, # lastNonPositive(lexeme.realization['feet'][0]),
				'_duration': incrementPairs[i][1],
				'parent': lexeme,
			}
			pickup['_pitches'] = lexeme.realization['outline'][:len(pickup['_offsets'])]
			station['_pitches'] = lexeme.realization['outline'][len(pickup['_offsets']):]
			pickup['_lens'] = lexeme.realization['lens'][:len(pickup['_offsets'])]
			station['_lens'] = lexeme.realization['lens'][len(pickup['_offsets']):]
			# for ligatures with multiple feet, add remaining feet, with internal offset
			if len(lexeme.realization['feet']) > 1:
				for index in range(1, len(lexeme.realization['feet'])):
					internalOffset = sum(passage.durations[i][0:index])
					station['_offsets'].extend([ offset+internalOffset for offset in lexeme.realization['feet'][index] ])
			splitLexemes.append(pickup)
			splitLexemes.append(station)

		# now go through and group lexeme increments by measure
		measureGroups = [ [splitLexemes[0]] ] # pickup to first measure will be padded to correct length of pickup measure
		measureDurations = [measure.barDuration.quarterLength for measure in measures[1:]]

		counter = 0.0
		bundle = []
		measureDuration = measureDurations.pop(0)
		for i in range(1, len(splitLexemes)):
			bundle.append(splitLexemes[i])
			counter += abs(splitLexemes[i]['_duration'])
			if counter == measureDuration:
				measureGroups.append(bundle)
				counter = 0.0
				bundle = []
				if i < len(splitLexemes)-1:
					measureDuration = measureDurations.pop(0)
		print("\nmeasureGroups")
		pprint(measureGroups)

		# for each measure bundle
		# recalculate all offsets relative to barline, find durations
		# insert into m21 measure object for rendering
		for i, measureGroup in enumerate(measureGroups):
			measure = measures[i]
			measureOffsets = []
			internalOffset = 0.0
			for j, increment in enumerate(measureGroup):
				# if duration is negative, is pickup
				if increment['_duration'] < 0:
					noteEndpoints = copy(increment['_offsets'])
					# calculate duration of last note accurately
					noteEndpoints.append(increment['_nextOffset'])
					durations = [ fl(x-y) for y, x in zip(noteEndpoints[:-1], noteEndpoints[1:]) ]
					# subtract from end of increment to find offsets
					internalOffset += abs(increment['_duration'])
					# special case for pickup bar - use duration including hidden leading rest
					if i==0 and j==0:
						internalOffset = measure.barDuration.quarterLength
					for k, duration in enumerate(durations):
						n = m21.note.Note()
						n.quarterLength = duration
						n.pitch = m21.pitch.Pitch()
						n.pitch.ps = 72.0 + increment['_pitches'][k] + increment['_lens'][k]
						noteOffset = internalOffset+increment['_offsets'][k]
						# measure.append(n)
						measure.insert(noteOffset, n)
				# if duration is positive, is station
				if increment['_duration'] > 0:
					noteEndpoints = copy(increment['_offsets'])
					# calculate duration of last note accurately
					noteEndpoints.append(abs(increment['_duration']))
					durations = [ fl(x-y) for y, x in zip(noteEndpoints[:-1], noteEndpoints[1:]) ]
					# add to beginning of increment to find offsets
					for k, duration in enumerate(durations):
						n = m21.note.Note()
						n.quarterLength = duration
						n.pitch = m21.pitch.Pitch()
						n.pitch.ps = 72.0 + increment['_pitches'][k] + increment['_lens'][k]
						noteOffset = internalOffset+increment['_offsets'][k]
						# measure.append(n)
						measure.insert(noteOffset, n)
					internalOffset += abs(increment['_duration'])
			if i == 0:
				measure.padAsAnacrusis()
			measure.makeRests(fillGaps=True, timeRangeFromBarDuration=True)
			measure.timeSignature = measure.bestTimeSignature()
		measures.show()
		# measures.show('lily')

timeSignatures = {
	1.5: m21.meter.TimeSignature('3/8'),
	2.0: m21.meter.TimeSignature('2/4'),
	2.5: m21.meter.TimeSignature('5/8'),
	3.0: m21.meter.TimeSignature('3/4'),
	3.5: m21.meter.TimeSignature('7/8'),
	4.0: m21.meter.TimeSignature('4/4'),
	4.5: m21.meter.TimeSignature('9/8'),
	5.0: m21.meter.TimeSignature('5/4'),
	5.5: m21.meter.TimeSignature('11/8'),
	6.0: m21.meter.TimeSignature('6/4'),
	6.5: m21.meter.TimeSignature('13/8'),
	7.0: m21.meter.TimeSignature('7/4'),
	7.5: m21.meter.TimeSignature('15/8'),
	8.0: m21.meter.TimeSignature('8/4'),
	8.5: m21.meter.TimeSignature('17/8'),
	9.0: m21.meter.TimeSignature('9/4'),
	9.5: m21.meter.TimeSignature('19/8'),
	10.0: m21.meter.TimeSignature('10/4'),
	10.5: m21.meter.TimeSignature('21/8'),
	11.0: m21.meter.TimeSignature('11/4'),
	11.5: m21.meter.TimeSignature('23/8'),
	12.0: m21.meter.TimeSignature('12/4'),
}

timeSignatures[2.5].beamSequence.partition(['3/8', '2/8'])
# timeSignatures[2.5].beamSequence.partition(['2/8', '3/8'])

# timeSignatures[8.0].beamSequence.partition(['1/4', '1/4', '1/4', '1/4', '1/4', '1/4', '1/4', '1/4'])
# for i in range(len(timeSignatures[8.0].beamSequence)):
#     timeSignatures[8.0].beamSequence[i] = timeSignatures[8.0].beamSequence[i].subdivide(['1/8', '1/8'])

timeSignatures[8.0].beamSequence.partition(['2/4', '2/4', '2/4', '2/4'])
for i in range(len(timeSignatures[8.0].beamSequence)):
    timeSignatures[8.0].beamSequence[i] = timeSignatures[8.0].beamSequence[i].subdivide(['1/4', '1/4'])
    for j in range(len(timeSignatures[8.0].beamSequence[i])):
        timeSignatures[8.0].beamSequence[i][j] = timeSignatures[8.0].beamSequence[i][j].subdivide(2)

timeSignatures[5.0].beamSequence.partition(['3/4', '2/4'])
timeSignatures[5.0].beamSequence[0] = timeSignatures[5.0].beamSequence[0].subdivide(['1/4', '1/4', '1/4'])
timeSignatures[5.0].beamSequence[1] = timeSignatures[5.0].beamSequence[1].subdivide(['1/4', '1/4'])

# timeSignatures[5.0].beamSequence.partition(['2/4', '3/4'])
# timeSignatures[5.0].beamSequence[0] = timeSignatures[5.0].beamSequence[1].subdivide(['1/4', '1/4'])
# timeSignatures[5.0].beamSequence[1] = timeSignatures[5.0].beamSequence[0].subdivide(['1/4', '1/4', '1/4'])
