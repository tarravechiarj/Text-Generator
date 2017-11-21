import json
import random

class TextGenerator:
    """Given a source file, generates randomized text with Markov chains"""
    
    def __init__(self, filename=None):
        self.resetCorpus()
        if filename is not None:
            self.setCorpus(filename)


    def resetCorpus(self):
        self.files = set()
        self.words = dict()
        self.followCounts = dict()


    def setCorpus(self, filename):
        self.resetCorpus()
        
        dictionaries = self._loadJSON(filename)
        if dictionaries is not None:
            self.words =  dictionaries[0]
            self.followCounts = dictionaries[1]
        else:
            self._updateDictionaries(filename)
            self._saveJSON(filename)
        
        self.files.add(filename)


    def addToCorpus(self, filename):
        self.files.add(filename)
        setFilename = "_".join(sorted(self.files))
        
        combined = self._loadJSON(setFilename)
        if combined is not None:
            self.words = combined[0]
            self.followCounts = combined[1]
        else:
            alone = self._loadJSON(filename)
            if alone is None:
                self._updateDictionaries(filename)
            else:
                self._combineDictionaries(alone[0], alone[1])
            self._saveJSON(setFilename)


    def _updateDictionaries(self, filename):
        def readWords(fileObj):
            for line in fileObj:
                for word in line.strip().split():
                    yield word
        try:
            with open(filename) as f:
                getWords = readWords(f)
                curr = next(getWords, None)
                while curr is not None:
                    n = next(getWords, None)
                    currDict = self.words.setdefault(curr, {})               
                    currDict[n] = currDict[n] + 1 if n in currDict else 1
                    self.followCounts.setdefault(curr, 0)
                    self.followCounts[curr] += 1
                    curr = n        
        
        except IOError as e:
            print("Error({0}): {1}".format(e.errno, e.strerror))


    def _combineDictionaries(self, wordsMap, countMap):
        for k,v in wordsMap.items():
            if k not in self.words:
                self.words[k] = v
            else:
                for word, count in v.items():
                    if word in self.words[k]:
                        self.words[k][word] += count
                    else:
                        self.words[k][word] = count
        for k,v in countMap.items():
            if k not in self.followCounts:
                self.followCounts[k] = v
            else:
                self.followCounts[k] += v


    def getSuffix(self, prefix):
        wordsEntry = self.words.get(prefix)
        if wordsEntry is None:
            return None       
        n = random.random()
        for followingWord in wordsEntry:
            count = wordsEntry.get(followingWord)
            total = self.followCounts[prefix]
            prob = count / total
            if n <= prob:
                return followingWord
            n = n - prob


    def textGenerator(self, prefix=None, maxSentenceLength=15):
        if maxSentenceLength <= 0:
            return
        if prefix is None:
            prefix = random.choice([key for key in self.words])

        yield prefix
        
        for i in range(1, maxSentenceLength):
            suffix = self.getSuffix(prefix)
            if suffix is None:
                return
            prefix = suffix
            yield suffix
 

    def printText(self, prefix=None, sentenceLength=15, lineLength=80):
        text = []
        
        charsInLine = 0
        for w in self.textGenerator(prefix, sentenceLength):
            wlen = len(w)
            if wlen + charsInLine > lineLength:
                text.append("\n" + w)
                charsInLine = wlen
            else:
                text.append(w)
                charsInLine += wlen
            # Take account of spaces to be added between words
            charsInLine += 1
        
        print(" ".join(text))


    def _loadJSON(self, filename):
        try:
            with open("json/" + filename + ".words") as wordsFile:
                dict1 = json.load(wordsFile)
            with open("json/" + filename + ".counts") as countsFile:
                dict2 = json.load(countsFile)
            return (dict1, dict2)
        except:
            return None


    def _saveJSON(self, filename):
        try:
            with open("json/" + filename + ".words", 'w') as wordsFile:
                json.dump(self.words, wordsFile)
            with open("json/" + filename + ".counts", 'w') as countsFile:
                json.dump(self.followCounts, countsFile)
        except Exception as e:
            print("Error({0}): {1}".format(e.errno, e.strerror))


