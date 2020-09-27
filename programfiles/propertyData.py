import nltk
from nltk import sent_tokenize, WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from .nounCategories import NounCategories
from .aProperty import AProperty
import spacy

class PropertyData:
    def __init__(self):
        '''Extracts term frequency information about the description of each property.

            Variables: 
            self.data (list): stores all the registered noun-adj|num instances and their frequencies 
            self._vectorized_data (defaultdict): dictionary with vectorized data
            self._lemmatizer (WordNetlemmatizer()): lemmatizer for normalization

        '''

        self.data = set()
        self._vectorized_data = None
        self._nlp = spacy.load('en_core_web_sm')
        self._lemmatizer = WordNetLemmatizer() 

  

    def normalize_if_num(self, num):
        '''Given a string-representation of a number returns the numeric representation

        Parameters:
        num (str): token to convert

        Returns:
        str: numeric representation of the inputstring
        
        '''

        nums_str = ['one', 'two', 'three', 'four', 'five', 'six', 'seven'
                'eight', 'nine']
        nums_int = [i+1 for i in range(9)]
        
        if num in nums_str:
            return str(nums_int[nums_str.index(num)])
        else:
            return num

            
    def vectorize(self, penalty=0.5):
            '''Given a list of bigrams makes a vectorized version of the data in the list. Nouns that occour with adj|num are
            given the vector 1, nouns that appear alone are penalized . Also builds a dicitonary mapping nouns and adj|num to each category.

                Parameters:
                c (NounCategories): NounCategories object containing categories
                p (AllProperties): AllProperties objects to analyze
                penalty (float): the penlaty for the (noun, None) 

            '''
            try:
                assert isinstance(penalty, float)
                assert penalty <= 1

            except AssertionError:
                raise ValueError("Penalty must be a float in the range 0.0 - 1.0")

            else:

                self._vectorized_data = Counter()
                
                for bigram in self.data: 

                    if bigram[1]:
                        self._vectorized_data[bigram] = 1
                    else:
                        self._vectorized_data[bigram] = 1-penalty
            
            return self._vectorized_data
            
            
    def extract(self, c, p):
        '''Finds adjectives and numbers applying to nouns if interest for each property and saves them as bigrams (noun, adj|num). 

            Parameters:
            c (NounCategories): NounCategories object containing categories
            p (AProperty): AProperty object to analyze

        '''

        try:
            assert isinstance(c, NounCategories)

        except AssertionError:
            raise ValueError("NounCategory object expected.")

        try:
            assert isinstance(p, AProperty)
        
        except AssertionError:
            raise ValueError("AProperty object expected.")

        try:
            assert p.get_p_description() != None
        
        except AssertionError:
            raise ValueError("Property description missing")
        

        else:
            nouns_of_interest = [noun for nounlist in c.get_categories().values() for noun in nounlist]

            custom_text = p.get_p_description()
            sentences = sent_tokenize(custom_text.lower())

            if p.get_data() is not None:
                self.data = p.get_data().data

            for sent in sentences:

                dep = self._nlp(sent)

                last = None
                ngram = ''

                for i, token in enumerate(dep):

                    token_text_lemma = self._lemmatizer.lemmatize(token.text) 
                    ngram_lemma = self._lemmatizer.lemmatize(ngram)

                    #add the nouns of interest to self.data to have some more vectors to work with later
                    if ngram in nouns_of_interest:
                        self.data.add((ngram, None))

                    elif ngram_lemma in nouns_of_interest:
                        self.data.add((ngram_lemma, None))
                        
                    else:
                        if token.text in nouns_of_interest:
                                self.data.add((token.text, None))

                        elif token_text_lemma in nouns_of_interest:
                            self.data.add((token_text_lemma, None))
                    
        
                    if ngram in nouns_of_interest:
                        self.data.add((ngram, None))

                    if last:
                        ngram = last + ' ' + token.text
            
                    last = token.text
            
                    possible_adj_nums = set()

                    left = [token for token in dep[i].lefts]
                    right = [token for token in dep[i].rights]

                    possible_adj_nums = left + right

                    for t in possible_adj_nums:

                        if t.tag_ in ['JJ', 'CD']:
                            adj_num =  self.normalize_if_num(t.text)

                            if ngram in nouns_of_interest:
                                self.data.add((ngram, adj_num))

                            elif ngram_lemma in nouns_of_interest:
                                self.data.add((ngram_lemma, adj_num))
                                
                            else:
                
                                if token.text in nouns_of_interest:
                
                                    self.data.add((token.text, adj_num))

                                elif token_text_lemma in nouns_of_interest:            
                                    self.data.add((token_text_lemma, adj_num))
