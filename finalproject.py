#
# finalproject.py (Final project)
#
# Building an initial text model
#
# Computer Science 111
#
import math

def clean_text(txt):
    """takes a string of text txt as a parameter and returns a list 
    containing the words in txt after it has been “cleaned”."""
    s = txt.lower()
    for symbol in """.,?"'!;:""":
        s = s.replace(symbol, '')

    s = s.split(' ')
    return s

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.
    
def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)    

def stem(s):
    """accepts a string as a parameter. The function should then return 
    the stem of s. The stem of a word is the root part of the word, 
    which excludes any prefixes and suffixes."""
    if s[-3:] == 'ies':
        s = s[:-3] + 'i'
    elif s[-3:] == 'ner':
        s = s[:-3] + 'i'
    elif s[-3:] == 'ing':
        if len(s) > 5:
            if s[-4] == s[-5]:
                s = s[:-4]
        else:
            s = s[:-3]
    elif s[-1:] == 'e':
        if s[:-1] == 'th':
            s = s[:-1] + 'e'
        else:
            s = s[:-1]
    elif s[-1:] == 'y' and s[:-1] == 'beaut':
                s = s[:-1]
    elif s[-1:] == 'y':
        s = s[:-1] + 'i'
    elif s[-2:] == 'er':
        s = s[:-2]
    elif s[-2:] == 'ed':
        s = s[:-2]
    elif s[-3:] == 'ier':
        s = s[:-3]
    elif s[:3] == 'pre':
        s = s[3:]
    elif s[:2] == 're':
        s = s[2:]
    elif s[-4:] == 'iers':
        s = s[:-4] + 'i'
    elif s[-1:] == 's':
        s = s[:-1]
    elif s[-3:] == 'ful':
        s = s[:-3]
        if s[-3:] == 'ing':
            if s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]
    elif s[-4:] == 'less':
        s = s[:-4]
        if s[-3:] == 'ing':
            if s[-4] == s[-5]:
                s = s[:-4]
            else:
                s = s[:-3]
    elif s[-4:] == 'ness':
        if s[-7:-4] == 'ful':
            s = s[:-7]
            if s[-3:] == 'ing':
                if s[-4] == s[-5]:
                    s = s[:-4]
                else:
                    s = s[:-3]
        elif s[-8:-4] == 'less':
            s = s[:-8]
            if s[-3:] == 'ing':
                if s[-4] == s[-5]:
                    s = s[:-4]
                else:
                    s = s[:-3]
        else:
            s = s[:-4]
    return s 

def compare_dictionaries(d1, d2):
    """It should take two feature dictionaries d1 and d2 as inputs, and 
    it should compute and return their log similarity score – using 
    the procedure described above."""
    score = 0
    total = 0
    if d1 == {}:
        return -50
    for key1 in d1:
        total += d1[key1]
    for key2 in d2:
        if key2 in d1:
            score += math.log(d1[key2] / total) * d2[key2]
        else:
            score += math.log(.5 / total) * d2[key2]
    return score
            
            
            

class TextModel:
    def __init__(self, model_name):
        """constructs a new TextModel object by accepting a string model_name 
        as a parameter and initializing the following three attributes:"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.every_space = {}
        
    def __repr__(self):
        """returns a string that includes the name of the model as well as the 
        sizes of the dictionaries for each feature of the text."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: '+ str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of every_space: ' + str(len(self.every_space)) + '\n'
        return s
    
    def add_string(self, s):
        """adds a string of text s to the model by augmenting the feature 
        dictionaries defined in the constructor. 
        It should not explicitly return a value."""
        o = 1
        for q in s:
            if q == ' ':
               o += 1
            if q in '.?!':
                if o not in self.sentence_lengths:
                    self.sentence_lengths[o] = 1
                else:
                    self.sentence_lengths[o] += 1 
                o = 0
        for t in s:
            if t not in self.every_space:
                self.every_space[t] = 1
            else:
                self.every_space[t] += 1
        word_list = clean_text(s)
        x = stem(word_list)
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
       
        for y in x:
            if stem(y) not in self.stems:
                self.stems[stem(y)] = 1
            else:
                self.stems[stem(y)] += 1


            
    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the 
        model. It should not explicitly return a value."""
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        s = f.read()
        self.add_string(s)
        f.close()
        
    

    def save_model(self):
        """saves the TextModel object self by writing its various feature
        dictionaries to files. There will be one file written for each 
        feature dictionary."""
        d = self.words   # Create a sample dictionary.
        words_name = self.name + '_' +'words'
        f = open(words_name, 'w')      # Open file for writing.
        f.write(str(d))              # Writes the dictionary to the file.
        f.close()

        d1 = self.word_lengths   # Create a sample dictionary.
        wordlengths_name = self.name + '_' + 'word_lengths'
        f1 = open(wordlengths_name, 'w')      # Open file for writing.
        f1.write(str(d1))              # Writes the dictionary to the file.
        f1.close()
        
        d3 = self.stems   # Create a sample dictionary.
        stems_name = self.name + '_' + 'stems'
        f3 = open(stems_name, 'w')      # Open file for writing.
        f3.write(str(d3))              # Writes the dictionary to the file.
        f3.close()
        
        d4 = self.sentence_lengths   # Create a sample dictionary.
        sentencelengths_name = self.name + '_' + 'sentence_lengths'
        f4 = open(sentencelengths_name, 'w')      # Open file for writing.
        f4.write(str(d4))              # Writes the dictionary to the file.
        f4.close()
        
        d7 = self.every_space   # Create a sample dictionary.
        everyspace_name = self.name + '_' + 'every_space'
        f7 = open(everyspace_name, 'w')      # Open file for writing.
        f7.write(str(d7))              # Writes the dictionary to the file.
        f7.close()
        
    def read_model(self):
        """reads the stored dictionaries for the called TextModel object 
        from their files and assigns them to the attributes of the 
        called TextModel."""
        words_name = self.name + '_words'
        f = open(words_name, 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()

        self.words = dict(eval(d_str))      # Convert the string to a dictionary.
        print("Inside the newly-read dictionary, d, we have:")
        print(self.words)  
        
        wordlengths_name = self.name + '_word_lengths'
        f2 = open(wordlengths_name, 'r')    # Open for reading.
        d2_str = f2.read()           # Read in a string that represents a dict.
        f2.close()

        self.word_lengths = dict(eval(d2_str))      # Convert the string to a dictionary.

        print("Inside the newly-read dictionary, d2, we have:")
        print(self.word_lengths)    

        stems_name = self.name + '_stems'
        f5 = open(stems_name, 'r')    # Open for reading.
        d5_str = f5.read()           # Read in a string that represents a dict.
        f5.close()

        self.stems = dict(eval(d5_str))      # Convert the string to a dictionary.

        print("Inside the newly-read dictionary, d5, we have:")
        print(self.stems)    
        
        sentencelengths_name = self.name + '_sentence_lengths'
        f6 = open(sentencelengths_name, 'r')    # Open for reading.
        d6_str = f6.read()           # Read in a string that represents a dict.
        f6.close()

        self.sentence_lengths = dict(eval(d6_str))      # Convert the string to a dictionary.

        print("Inside the newly-read dictionary, d6, we have:")
        print(self.sentence_lengths)   
        
        everyspace_name = self.name + '_every_space'
        f8 = open(everyspace_name, 'r')    # Open for reading.
        d8_str = f8.read()           # Read in a string that represents a dict.
        f8.close()

        self.every_space = dict(eval(d8_str))      # Convert the string to a dictionary.

        print("Inside the newly-read dictionary, d8, we have:")
        print(self.every_space)  
        
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores 
        measuring the similarity of self and other – one score 
        for each type of feature (words, word lengths, stems, 
        sentence lengths, and your additional feature)."""
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        every_space_score = compare_dictionaries(other.every_space, self.every_space)
        s = [word_score, word_lengths_score, stems_score, sentence_lengths_score, every_space_score]
        return s
    
    def classify(self, source1, source2):
        """compares the called TextModel object (self) to two other 
        “source” TextModel objects (source1 and source2) and determines 
        which of these other TextModels is the more likely source of the
        called TextModel."""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for source1' + ':', scores1)
        print('scores for source2' + ':', scores2)
        x = 0
        y = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                x += 1
            elif scores1[i] < scores2[i]:  
                y += 1
        if x > y:
            print('mystery is more likely to have come from source3')
        elif x < y:
            print('mystery is more likely to have come from source4')
            
def test():
    """ Here is one function that you can use to test your TextModel 
    implementation: """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')
    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
    
    source3 = TextModel('source3')
    source3.add_file('12.txt')
    source3.add_file('3.txt')
    source3.add_file('4.txt')
    source3.add_file('5.txt')
    source4 = TextModel('source4')
    source4.add_file('6.txt')
    source4.add_file('7.txt')
    source4.add_file('8.txt')
    source4.add_file('9.txt')
    
    
    new1 = TextModel('new1')
    new1.add_file('10.txt')
    new1.add_file('111.txt')
    new1.add_file('122.txt')
    new1.add_file('13.txt')
    new1.classify(source3, source4)
    
    new2 = TextModel('new2')
    new2.add_file('333.txt')
    new2.classify(source3, source4)
    
    new3 = TextModel('new3')
    new3.add_file('444.txt')
    new3.classify(source3, source4)
    
    
    new4 = TextModel('new4')
    new4.add_file('555.txt')
    new4.classify(source3, source4)
   
    
    
    

    
        