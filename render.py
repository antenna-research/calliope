import music21 as m21
import datetime
import requests
from random import choice
from pprint import pprint
from copy import copy, deepcopy
from utils import *

class Renderer(object):
	""" turns feature spellout into score object, with processing """

	def render(self, passage, instrument):
		part = m21.stream.Part()
		inst = deepcopy(instruments[instrument])
		part.insert(0, inst)
		part.clef = inst.clef
		passage.fitToInstrument(inst)

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
		shift = 72
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
			if 'shift' in lexeme.realization:
				pickup['_shift'] = lexeme.realization['shift']
				station['_shift'] = lexeme.realization['shift']
				shift = lexeme.realization['shift']
			else:
				pickup['_shift'] = station['_shift'] = shift
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
				labels = self.makeLabels(str(increment['parent'].label))
				# if duration is negative, is pickup
				if increment['_duration'] < 0:
					noteEndpoints = copy(increment['_offsets'])
					# calculate duration of last note accurately
					noteEndpoints.append(increment['_nextOffset'])
					durations = [ fl(x-y) for y, x in zip(noteEndpoints[:-1], noteEndpoints[1:]) ]
					measure.insert(internalOffset, labels[0])
					# subtract from end of increment to find offsets
					internalOffset += abs(increment['_duration'])
					# special case for pickup bar - use duration including hidden leading rest
					if i==0 and j==0:
						internalOffset = measure.barDuration.quarterLength
					for k, duration in enumerate(durations):
						n = m21.note.Note()
						n.quarterLength = duration
						n.pitch = m21.pitch.Pitch()
						n.pitch.ps = increment['_pitches'][k] + increment['_lens'][k] + increment['_shift']
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
					measure.insert(internalOffset, labels[1])
					for k, duration in enumerate(durations):
						n = m21.note.Note()
						n.quarterLength = duration
						n.pitch = m21.pitch.Pitch()
						n.pitch.ps = increment['_pitches'][k] + increment['_lens'][k] + increment['_shift']
						noteOffset = internalOffset+increment['_offsets'][k]
						# measure.append(n)
						measure.insert(noteOffset, n)
					internalOffset += abs(increment['_duration'])
			if i == 0:
				measure.padAsAnacrusis()
			measure.makeRests(fillGaps=True, timeRangeFromBarDuration=True)
			measure.timeSignature = measure.bestTimeSignature()

		heading = self.makeHeading()
		part.insert(0, m21.metadata.Metadata())
		part.metadata.title = heading[0]
		part.metadata.composer = heading[1]
		part.show()
		# measures.show('lily')

	def makeLabels(self, text):
		pickup_label = m21.expressions.TextExpression( '\'' ) #  ( "·"+text )
		down_label = m21.expressions.TextExpression( text )
		down_label.style.fontSize = pickup_label.style.fontSize = 7.0
		down_label.style.absoluteY = pickup_label.style.absoluteY = 62
		down_label.style.fontStyle = pickup_label.style.fontStyle = 'italic'
		down_label.style.fontWeight = 'normal'
		pickup_label.style.fontWeight = 'normal'
		return (pickup_label, down_label)

	def makeHeading(self):
		# date in 'composer' slot
		now = datetime.datetime.now()
		timestamp = str(now.timestamp()).split('.')[0]
		date = now.strftime('%B %d, %Y ')+str(int(now.strftime('%I')))+now.strftime(':%M%p').lower()

		# timestamp serial and mnemonic random word in 'title' slot
		word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
		response = requests.get(word_site)
		words = response.content.splitlines()
		word = choice(words).decode("utf-8").capitalize()
		title = word+" · "+str(timestamp)
		return (title, date)

timeSignatures = {
	1.25: m21.meter.TimeSignature('5/16'),
	1.5: m21.meter.TimeSignature('3/8'),
	1.75: m21.meter.TimeSignature('7/16'),
	2.0: m21.meter.TimeSignature('2/4'),
	2.25: m21.meter.TimeSignature('9/16'),
	2.5: m21.meter.TimeSignature('5/8'),
	2.75: m21.meter.TimeSignature('11/16'),
	3.0: m21.meter.TimeSignature('3/4'),
	3.25: m21.meter.TimeSignature('13/16'),
	3.5: m21.meter.TimeSignature('7/8'),
	3.75: m21.meter.TimeSignature('15/16'),
	4.0: m21.meter.TimeSignature('4/4'),
	4.25: m21.meter.TimeSignature('17/16'),
	4.5: m21.meter.TimeSignature('9/8'),
	4.75: m21.meter.TimeSignature('19/16'),
	5.0: m21.meter.TimeSignature('5/4'),
	5.25: m21.meter.TimeSignature('21/16'),
	5.5: m21.meter.TimeSignature('11/8'),
	5.75: m21.meter.TimeSignature('23/16'),
	6.0: m21.meter.TimeSignature('6/4'),
	6.25: m21.meter.TimeSignature('25/16'),
	6.5: m21.meter.TimeSignature('13/8'),
	6.75: m21.meter.TimeSignature('27/16'),
	7.0: m21.meter.TimeSignature('7/4'),
	7.25: m21.meter.TimeSignature('29/16'),
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



instruments = {
	'violin': m21.instrument.Violin(),
	'viola': m21.instrument.Viola(),
	'cello': m21.instrument.Violoncello(),
	'double bass': m21.instrument.Contrabass(),
    'bass guitar': m21.instrument.ElectricBass(),
    'acoustic guitar': m21.instrument.ElectricGuitar(),
	'tuba': m21.instrument.Tuba(),
	'bass_trombone': m21.instrument.BassTrombone(),
	'french_horn': m21.instrument.Horn(),
	'trombone': m21.instrument.Trombone(),
    'trumpet': m21.instrument.Trumpet(),
	'piccolo': m21.instrument.Piccolo(),
	'flute': m21.instrument.Flute(),
	'alto_flute': m21.instrument.Flute(),
	'oboe': m21.instrument.Oboe(),
	'cor_anglais': m21.instrument.EnglishHorn(),
	'bassoon': m21.instrument.Bassoon(),
	'contrabassoon': m21.instrument.Bassoon(),
	'clarinet': m21.instrument.Clarinet(),
	'bass_clarinet': m21.instrument.BassClarinet(),
	'soprano_recorder': m21.instrument.Recorder(),
	'alto_recorder': m21.instrument.Recorder(),
	'tenor_recorder': m21.instrument.Recorder(),
	'bass_recorder': m21.instrument.Recorder(),
	'baritone': m21.instrument.BaritoneSaxophone(),
	'tenor': m21.instrument.TenorSaxophone(),
	'alto': m21.instrument.AltoSaxophone(),
	'soprano': m21.instrument.SopranoSaxophone(),
	'glockenspiel': m21.instrument.Glockenspiel(),
	# 'xylophone': m21.instrument.Xylophone(),
	'vibraphone': m21.instrument.Vibraphone(),
	'marimba': m21.instrument.Marimba(),
	'bass_marimba': m21.instrument.Marimba(),
	'celesta': m21.instrument.Celesta(),
	'tubular_bells': m21.instrument.TubularBells(),
	'timpani': m21.instrument.Timpani(),
    'harpsichord': m21.instrument.Harpsichord(),
	'harp': m21.instrument.Harp(),
}


instrumentRanges = {
	'violin': 32,
	'viola': 30,
	'cello': 32,
	'double bass': 39,
	'bass guitar': 39,
	'acoustic guitar': 48,
	'tuba': 30,
	'bass_trombone': 33,
	'french_horn': 43,
	'trombone': 32,
	'trumpet': 27,
	'piccolo': 26,
	'flute': 32,
	'alto_flute': 36,
	'oboe': 30,
	'cor_anglais': 29,
	'bassoon': 41,
	'contrabassoon': 31,
	'clarinet': 40,
	'bass_clarinet': 39,
	'soprano_recorder': 26,
	'alto_recorder': 26,
	'tenor_recorder': 26,
	'bass_recorder': 26,
	'baritone': 32,
	'tenor': 32,
	'alto': 32,
	'soprano': 32,
	'glockenspiel': 29,
	'xylophone': 43,
	'vibraphone': 36,
	'marimba': 51,
	'bass_marimba': 48,
	'celesta': 48,
	'tubular_bells': 17,
	'timpani': 15,
	'harpsichord': 60,
	'harp': 79,
}

instrumentClefs = {
	'violin': m21.clef.TrebleClef(),
	'viola': m21.clef.AltoClef(),
	'cello': m21.clef.BassClef(), # or tenor
	'double bass': m21.clef.BassClef(),
	'bass guitar': m21.clef.BassClef(),
	'acoustic guitar': m21.clef.TrebleClef(),
	'tuba': m21.clef.BassClef(),
	'bass_trombone': m21.clef.BassClef(),
	'french_horn': m21.clef.TrebleClef(), # or bass
	'trombone': m21.clef.BassClef(),
	'trumpet': m21.clef.TrebleClef(),
	'piccolo': 'treble^8',
	'flute': m21.clef.TrebleClef(),
	'alto_flute': m21.clef.TrebleClef(),
	'oboe': m21.clef.TrebleClef(),
	'cor_anglais': m21.clef.TrebleClef(),
	'bassoon': m21.clef.BassClef(), # tenor
	'contrabassoon': m21.clef.BassClef(),
	'clarinet': m21.clef.TrebleClef(),
	'bass_clarinet': m21.clef.TrebleClef(), # or bass
	'soprano_recorder': m21.clef.TrebleClef(),
	'alto_recorder': m21.clef.TrebleClef(),
	'tenor_recorder': m21.clef.TrebleClef(),
	'bass_recorder': m21.clef.BassClef(),
	'baritone': m21.clef.TrebleClef(),
	'tenor': m21.clef.TrebleClef(),
	'alto': m21.clef.TrebleClef(),
	'soprano': m21.clef.TrebleClef(),
	# todo: engrave voice to grand staff
	'glockenspiel': m21.clef.TrebleClef(),
	# 'xylophone': m21.clef.TrebleClef(),
	'vibraphone': m21.clef.TrebleClef(),
	'marimba': m21.clef.TrebleClef(),
	'bass_marimba': m21.clef.TrebleClef(),
	'celesta': m21.clef.TrebleClef(),
	'tubular_bells': m21.clef.TrebleClef(),
	'timpani': m21.clef.TrebleClef(),
	'harpsichord': m21.clef.TrebleClef(),
	'harp': m21.clef.TrebleClef(),
}

def initializeInstruments():
	# add highestNote, clef, ...
	for name in instruments:
		inst = instruments[name]
		inst.name = name
		print(name)
		inst.highestNote = m21.pitch.Pitch()
		if name in ['glockenspiel','vibraphone','marimba','bass_marimba','celesta','tubular_bells','timpani']:
			inst.lowestNote = m21.pitch.Pitch()
		if name == 'glockenspiel' or name == 'vibraphone':
			inst.lowestNote.ps = 65
		if name == 'marimba':
			inst.lowestNote.ps = 60
		if name == 'bass_marimba':
			inst.lowestNote.ps = 48
		if name == 'bass_marimba':
			inst.lowestNote.ps = 48
		if name == 'celesta' or name == 'tubular_bells':
			inst.lowestNote.ps = 72
		if name == 'timpani':
			inst.lowestNote.ps = 50
		inst.highestNote.ps = inst.lowestNote.ps + instrumentRanges[name]
		inst.clef = instrumentClefs[name]

initializeInstruments()

def inst(inst_name):
	return copy(instruments[inst_name])