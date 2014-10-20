from hyphen import Hyphenator
import json
from haikutagger import tokenize_dataset,tokenize_haiku, pick_random_structure
import pattern.en as pt

HAIKU_LINES = 3
HAIKU_SYLLABLES = [5, 7, 5]

def ghaiku(grammar_tree,meaning_generator):
	haiku = ''
	oldWords = [meaning_generator.random_word('NN')]
	# generate POS tags and words at the same time
	i = 2
	oldWords = []
	# starting distribution
	start = grammar_tree.random_pick(grammar_tree._root)
	POSlist = [start[0],start[1]]
	word1 = wordFromPOStag(POSlist[0],oldWords,meaning_generator)
	oldWords += [word1]
	word2 = wordFromPOStag(POSlist[1],oldWords,meaning_generator)
	oldWords += [word2]
	syllables = count_syllables(word1)+count_syllables(word2)
	haiku += word1+' '+word2+' '
	for line in xrange(0,HAIKU_LINES):
		syllables = 0
		while syllables <= HAIKU_SYLLABLES[line]:
			POSlist += [grammar_tree.random_pick(grammar_tree.get_successors((POSlist[i-2],POSlist[i-1])))]
			newWord = wordFromPOStag(POSlist[-1],oldWords,meaning_generator)
			haiku += newWord+' '
			oldWords += [newWord]
			syllables += count_syllables(newWord)
		haiku += '\n'
	print(haiku)

def guessLineBreaksHaiku(grammar_tree,meaning_generator):
	start = grammar_tree.random_pick(grammar_tree._root)
	POSlist = [start[0],start[1]]
	for i in xrange(2,10):
		POSlist += [grammar_tree.random_pick(grammar_tree.get_successors((POSlist[i-2],POSlist[i-1])))]

	# guess line breaks
	POSlist = guessLineBreaks(POSlist)
	# generate words
	haiku = ''
	oldWords = [meaning_generator.random_word()]
	for postag in POSlist:
		newWord = wordFromPOStag(postag,oldWords,meaning_generator)
		oldWords += [newWord]
		haiku += newWord+' '
	print(haiku)

def guessFromGrammarStructs(meaning_generator):
	NUM_HAIKUS = 600
	with open('haikus.json') as haikus_file:
		dataset = json.load(haikus_file)
	pos_counter = tokenize_dataset(dataset, haikus_limit=NUM_HAIKUS)
	pos_tags = []
	for i in xrange(3):
		grammar_struct = pick_random_structure(pos_counter)
		pos_tags += list(grammar_struct)	
		print(grammar_struct)
		pos_tags += ['\n']
	
	haiku = ''
	oldWords = [meaning_generator.random_word('NN')]
	for postag in pos_tags:
		newWord = wordFromPOStag(postag,oldWords,meaning_generator)
		oldWords += [newWord]
		haiku += newWord+' '
	print(haiku)


def shapeNoun(noun,posTag):
	"""
	Reshapes the base noun according to it's pos tag
	Assuming noun is in singular form
	"""
	if posTag == 'NNS' or posTag == 'NNPS':
		return pt.pluralize(noun)
	else:
		return pt.singularize(noun)

def shapeVerb(verb,posTag):
	"""
	Reshapes the verb to get proper grammar, like past, present etc etc
	"""
	print(verb,posTag,pt.conjugate(verb,posTag))
	return pt.conjugate(verb,posTag)


def wordFromPOStag(POStag,oldWords,meaning_generator):
	# some filler words
	fillers = {
	'DT':'the',
	'CC':'and',
	"PRP$":'its',
	'PRP':'me',	
	'IN':'at',
	'TO':'to',
	'RP': 'not', # off?
	'POS': '\'s',
	'MD':'can',
	'WRB':'who',
	'WP':'what',
	}
	newWord = POStag
	if fillers.has_key(POStag):
		newWord = fillers[POStag]+' '
	elif POStag.startswith('NN'): # TODO: make grammar absolutely correct
		newWord = shapeNoun(suitable_word(oldWords,'NN',meaning_generator),POStag)
	elif POStag.startswith('VB'):
		newWord = shapeVerb(suitable_word(oldWords,'VB',meaning_generator),POStag)
	elif POStag.startswith('RB'):
		newWord = suitable_word(oldWords,'RB',meaning_generator)
	elif POStag.startswith('JJ'):
		newWord = suitable_word(oldWords,'JJ',meaning_generator)
	return unicode(newWord)


def suitable_word(oldWords,POStag,meaning_generator):
	for x in xrange(1,3):
		for word in oldWords:
			newWord = meaning_generator.associate(word,POStag)
			if newWord != None and newWord not in oldWords:
				return newWord
	# couldn't find any, let's just return random word
	return meaning_generator.random_word(POStag)

def guessLineBreaks(POStags):
	toReturn = POStags[0:1]
	lastTag = None
	lineLen = 1
	for i in xrange(1,len(POStags)):
		if lineLen > 4:
			toReturn += ['\n']
			lineLen = 1
		elif lineLen > 1:
			if POStags[i-1].startswith('NN') and POStags[i].startswith('NN'):
				toReturn += ['\n']
				lineLen = 1
			elif POStags[i-1].startswith('JJ') and POStags[i].startswith('JJ'):
				toReturn += ['\n']
				lineLen = 1
			elif POStags[i] == 'DT':
				toReturn += ['\n']
				lineLen = 1
		else:
			lineLen += 1

		toReturn += [POStags[i]]
	return toReturn

def count_syllables(word):
	hyphenator = Hyphenator('en_US')
	return max(len(hyphenator.syllables(word)),1)