import csv
import random
import nltk

class WAN:

	def __init__(self,fileName="wan.csv"):
		f = open(fileName)
		f.readline() # skip first line, the header line
		r = csv.reader(f)
		assoc = {}
		for n in r: # probably worse pos_tagging since we're out of context
			if assoc.has_key(n[0]):
				assoc[n[0]] = assoc[n[0]] + [n[1]] #nltk.pos_tag([n[1]])
			else:
				assoc[n[0]] = [n[1]] # nltk.pos_tag([n[1]])
			#print(assoc[n[0]])
		self._assoc = assoc

	# returns a random word that has at least one association
	def random_word(self,POStag='NN'):
		return self._assoc.keys()[int(random.random()*len(self._assoc.keys()))]


	# returns None if no associations could be found
	def associate(self,word,POStag='NN'):
		if self._assoc.has_key(word) == False:
			return None
		else:
			candidates = [a for a in self._assoc[word]]
			if len(candidates) == 0:
				return None
			else: # return random associated word
				return candidates[int(random.random()*len(candidates))]


if __name__ == '__main__':
	wan = WAN()
	seed = 'NATURE'
	print(seed,wan.associate(seed))