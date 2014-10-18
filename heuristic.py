
def ghaiku(grammar_tree,meaning_generator):
	# some filler words
	fillers = {
	'DT':'the',
	'CC':'and',
	"PRP$":'its',
	'PRP':'me',
	'IN':'from',
	'TO':'to',
	'RP': 'not', # off?
	'POS': '\'s',
	'MD':'can',
	'WRB':'who',
	}
	# starting distribution
	start = grammar_tree.random_pick(grammar_tree._root)
	POSlist = [start[0],start[1]]
	# generate POS tags
	for i in xrange(2,10):
		POSlist += [grammar_tree.random_pick(grammar_tree.get_successors((POSlist[i-2],POSlist[i-1])))]
	print(POSlist)
	# get some linebreaks
	POSlist = guessLineBreaks(POSlist)
	# fill in the blanks
	haiku = ''
	oldWords = [meaning_generator.random_word('NN')]
	for x in POSlist:
		newWord = x
		if fillers.has_key(x):
			newWord = fillers[x]+' '
		elif x.startswith('NN'): # TODO: make grammar absolutely correct
			newWord = suitable_word(oldWords,'NN',meaning_generator)
		elif x.startswith('VB'):
			newWord = suitable_word(oldWords,'VB',meaning_generator)
		elif x.startswith('RB'):
			newWord = suitable_word(oldWords,'RB',meaning_generator)
		elif x.startswith('JJ'):
			newWord = suitable_word(oldWords,'JJ',meaning_generator)
		haiku += newWord+' '
		oldWords += [newWord]
	print(haiku)

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
	for i in xrange(1,len(POStags)-1):
		if POStags[i-1].startswith('NN') and POStags[i].startswith('NN'):
			toReturn += ['\n']
		elif POStags[i] == 'DT':
			toReturn += ['\n']
		toReturn += [POStags[i]]
	return toReturn


