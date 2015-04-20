import csv
import random
import nltk

class WAN:

	def __init__(self,fileName="wan.csv"):
		f = open(fileName)
		f.readline() # skip first line, the header line
		r = csv.reader(f)
		assoc = {}
		for n in r:
			key = n[0].lower().strip()
			value = n[1].lower().strip()
			if assoc.has_key(key):
				assoc[key] = assoc[key] + [value]
			else:
				assoc[key] = [value]
		self._assoc = assoc
		self._POSmap = {'NN':'n','VB':'v','JJ':'a','RB':'r'}

	# returns a random word that has at least one association
	def random_word(self,POStag='NN'):
		while True:
			word = self._assoc.keys()[int(random.random()*len(self._assoc.keys()))]
			if self.__has_POS_tag(word,POStag):
			 	return word
			# if self.__has_POS_tag(word,POStag):
			#  	return word


	def __has_POS_tag(self,word, POStag):
		# let's be more strict and only use first definition
		return nltk.pos_tag([word])[0][1] == POStag
		#return len(wn.synsets(word)) > 0 and wn.synsets(word)[0].pos() == self._POSmap[POStag]
		#return len([synset for synset in wn.synsets(word) if synset.pos() == self._POSmap[POStag]]) > 0


	# returns None if no associations could be found
	def associate(self,word,POStag='NN'):
		if self._assoc.has_key(word) == False:
			return None
		else:
			candidates = [a for a in self._assoc[word] if self.__has_POS_tag(a,POStag)]
			if len(candidates) == 0:
				return None
			else: # return random associated word
				return candidates[int(random.random()*len(candidates))]


if __name__ == '__main__':
	wan = WAN()
	seed = 'cold'
	print(seed,wan.associate(seed,'VB'))




