"""A feature extractor for crfsuite"""
import crfutils, sys, os, re
import string
# Separator of field values.
separator = '\t'
templates = []
fields = 'w y'

templates = (
    (('w', -1), ),
    (('w',  0), ),
    (('w', -1), ('w',  0)), 
    (('w',  0), ('w',  1)),
#    (('w',  -1), ('w', 0), ('w',  1)),   # new template to look at 3 words
    )

DF = None


class DictionaryFeatures:

    def log(self, s):
        print >> sys.stderr, s

    def __init__(self, dictDir):
        self.word2dictionaries = {}
        self.dictionaries = []
        i = 0
        for d in sorted(os.listdir(dictDir)):
            print >> sys.stderr, "read dict %s"%d
            self.dictionaries.append(d)
            if d == '.svn':
                continue
            for line in open(dictDir + "/" + d):
                word = line.rstrip('\n')
                word = word.strip(' ').lower()
                if not self.word2dictionaries.has_key(word):            
                    self.word2dictionaries[word] = str(i)
                else:
                    self.word2dictionaries[word] += "\t%s" % i
            i += 1
#        j=0
#        self.log("printing self.dictionaries ***********************")
#        for kk in self.dictionaries:
#                self.log(str(kk))
#        self.log("\n\nprinting self.word2dictionaries ***********************")
#        for kk in self.word2dictionaries.keys():
#            print >> sys.stderr, kk, self.word2dictionaries[kk]
#            j+=1
#            if j == 10:
#                break
        
    MAX_WINDOW_SIZE=6
    def GetDictFeatures(self, words, i):
        #print words
        #print i
        features = []
        for window in range(self.MAX_WINDOW_SIZE):
            for start in range(max(i-window+1, 0), i+1):
                end = start + window
                phrase = ' '.join(words[start:end]).lower().strip(string.punctuation)
                #print window,' ', start , ' ', end , ' ', phrase
                if self.word2dictionaries.has_key(phrase):
                    for j in self.word2dictionaries[phrase].split('\t'):
                        features.append('DICT=%s' % self.dictionaries[int(j)])
                        if window > 1:
                            features.append('DICTWIN=%s' % window)
        return list(set(features))

def GetOrthographicFeatures(word, goodCap=True):
    features = []

    features.append("word=%s" % word)
    features.append("word_lower=%s" % word.lower())
    if(len(word) >= 4):
        features.append("prefix=%s" % word[0:1].lower())
        features.append("prefix=%s" % word[0:2].lower())
        features.append("prefix=%s" % word[0:3].lower())
        features.append("suffix=%s" % word[len(word)-1:len(word)].lower())
        features.append("suffix=%s" % word[len(word)-2:len(word)].lower())
        features.append("suffix=%s" % word[len(word)-3:len(word)].lower())

    if re.search(r'^[A-Z]', word):
        features.append('INITCAP')
    if re.search(r'^[A-Z]', word) and goodCap:
        features.append('INITCAP_AND_GOODCAP')
    if re.match(r'^[A-Z]+$', word):
        features.append('ALLCAP')
    if re.match(r'^[a-z]+$', word):
        features.append('ALLSMALL')
    if re.match(r'^[A-Z]+$', word) and goodCap:
        features.append('ALLCAP_AND_GOODCAP')
    if re.match(r'.*[0-9].*', word):
        features.append('HASDIGIT')
    if re.match(r'[0-9]', word):
        features.append('SINGLEDIGIT')
    if re.match(r'[0-9][0-9]', word):
        features.append('DOUBLEDIGIT')
#    if re.match(r'the', word):
#        features.append('HASTHE')
    if re.match(r'[0-9][0-9][0-9]', word):
        features.append('TRIPPLEDIGIT')
    if re.match(r'.*-.*', word):
        features.append('HASDASH')
    if re.match(r'[.,;:?!-+\'"]', word): # ---added--- forward and backward slash with espace, now removed
        features.append('PUNCTUATION')
    return features

def Featurizer(X):
    #print 'Featurizer called with X ', X
    global DF
    if X:
        entire= []
        for t in range(len(X)):
            entire.append(X[t]['w'])
        for t in range(len(X)):
            w = X[t]['w']
            feats = DF.GetDictFeatures(entire,t) + GetOrthographicFeatures(w)
            for f in feats:
                X[t]['F'].append('%s'%(f))

def FeatureExtractor(X):
    """apply attribute templates to obtain features (in fact, attributes)"""
    #print 'FeatureExtractor called with X ', X
    crfutils.apply_templates(X, templates)
     
    Featurizer(X)
    #print X
    if X:
        #print 'in if X'
        X[0]['F'].append('__BOS__')     # BOS feature
        X[-1]['F'].append('__EOS__')    # EOS feature

if __name__ == '__main__':
    DF = DictionaryFeatures("./lexicon")
    #print 'Running main crf module ********************'
    crfutils.main(FeatureExtractor, fields=fields, sep=separator)
