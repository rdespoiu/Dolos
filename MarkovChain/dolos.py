from sys import argv, version_info
from random import choice
from time import time

PYTHON_VERSION = version_info.major

class Dolos:
	# With requested depth in mind, on init the input tweets are parsed and then a markov chain of all words is created.
	def __init__(self, tweets, depth, user):
		# Each word parsed from the input lexicon
		self.words = []

		# Chain data structure, with all options for string generation (i.e. the -> red -> fox -> jumped -> N)
		self.chain = dict()

		# Depth of nodes in the chain, specified in the config file. Good when looking to have some accurate sounding
		# phrases as opposed to a completely random jumble of words. Sugested depth is 3. Not too much, not too little.
		self.depth = depth

		# Parse tweets from input and append each word to the words array
		self.parseTweets(tweets)

		# Creates Markov chain from parsed tweets
		self.createChain(self.words, depth)

		# User being simulated
		self.user = user

	def __del__(self):
		print 'Successfully deallocated Dolos'

	# Simple parsing. Take each word from the input lexicon and append to the words array for chain mapping.
	def parseTweets(self, tweets):
		for tweet in tweets:
			for word in tweet.split(' '):
				if not ('http' in word or 'www' in word or '@' in word):
					self.words.append(word)

	# Iterates through each index of the words array and creates a chain of words from index 0 (relative to current position)
	# to the specified depth. This is done for each word in the array until all indices have been exhausted.
	def createChain(self, words, depth):
		index = 0
		freqTable = {}
		while index < len(words):
			currentLevel = freqTable
			for word in words[ index : index + depth + 1 ]:
				if word not in currentLevel:
					currentLevel[word] = {}
				currentLevel = currentLevel[word]
			index += 1
		self.chain = freqTable

	# Generates a tweet string based on the Markov chain generated earlier. Also utilizes input depth with regards to how long
	# continuous phrases should be when being pulled (by random choice) from the chain data structure.
	def generateTweet(self):
		string = str()
		currentDepth = 0
		seed = {}
		currentWord = str()

		while len(string) < 140:
			if not string:
				string = '{}: '.format(self.user)
				while not currentWord or not currentWord[0].isupper():
					currentWord = choice(list(self.chain.keys()))
			else:
				try:
					currentWord = choice(list(self.chain[currentWord].keys()))
				except KeyError:
					currentWord = choice(list(self.chain.keys()))

			seed = self.chain[currentWord]

			if len(string + currentWord) > 140:
				if len(string + '.') <= 140:
					string += '.'
				break

			string += currentWord + ' '

			while currentDepth < self.depth:
				try:
					currentWord = choice(list(seed.keys()))
				except KeyError:
					currentWord = choice(list(self.chain.keys()))
					break

				seed = seed[currentWord]
				if len(string + currentWord) > 140:
					if len(string + '.') <= 140:
						string += '.'
					break

				string += currentWord + ' '
				currentDepth += 1

			currentDepth = 0

		if not string.endswith(('.', '!', '?')) and len(string) < 140:
			if string.endswith(' '):
				string = string[0 : -1] + '.'
			else:
				string += "."

		return string
