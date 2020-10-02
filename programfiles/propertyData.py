import nltk
from nltk import sent_tokenize, WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from .nounCategories import NounCategories
from .property import Property
from typing import *
import spacy

class PropertyData:
    def __init__(self):
        """Extracts term frequency information about the description of each property.

            Variables: 
            self.data (list): stores all the registered noun-adj|num instances and their frequencies 
            self._vectorized_data (defaultdict): dictionary with vectorized data
            self._lemmatizer (WordNetlemmatizer()): lemmatizer for normalization

        """

        self.data = set()
        self._vectorized_data = None
        self._nlp = spacy.load('en_core_web_sm')
        self._lemmatizer = WordNetLemmatizer() 


    def normalize_if_num(self, num: str) -> str:
        """Given a string-representation of a number returns the numeric representation

        Parameters:
        num (str): token to convert

        Returns:
        str: numeric representation of the inputstring
        
        """

        nums_str = ['one', 'two', 'three', 'four', 'five', 'six', 'seven'
                'eight', 'nine']

        nums_int = [i+1 for i in range(9)]
        
        if num in nums_str:
            return str(nums_int[nums_str.index(num)])
        else:
            return num

            
    def vectorize(self, penalty: float=0.5) -> Counter:
            """Given a list of bigrams makes a vectorized version of the data in the list. Nouns that occour with adj|num are
            given the vector 1, nouns that appear alone are penalized . Also builds a dicitonary mapping nouns and adj|num to each category.

                Parameters:
                c (NounCategories): NounCategories object containing categories
                p (AllProperties): AllProperties objects to analyze
                penalty (float): the penlaty for the (noun, None) 

            """
          
            self._vectorized_data = Counter()
            
            for bigram in self.data: 

                if bigram[1]:
                    self._vectorized_data[bigram] = 1
                else:
                    self._vectorized_data[bigram] = 1-penalty
        
            return self._vectorized_data
            
            
    def extract(self, pos_tags: List[str], all_categories: NounCategories, a_property: Property):
        """Finds adjectives and numbers applying to nouns if interest for each property and saves them as bigrams (noun, adj|num). 

            Parameters:
            all_categories (NounCategories): NounCategories object containing categories
            a_property (Property): Property object to analyze

        """

        nouns_of_interest = [noun for nounlist in all_categories.get_categories().values() for noun in nounlist]
        document = a_property.get_p_description()
        sentences = sent_tokenize(document.lower())

        for sent in sentences:
            
            #---generate a dependecy parcing of the sentance---
            dep = self._nlp(sent)
            last = None
            ngram = ''

            for i, token in enumerate(dep):

                token_text_lemma = self._lemmatizer.lemmatize(token.text) 
                ngram_lemma = self._lemmatizer.lemmatize(ngram)

                #---add the nouns of interest to self.data to have some more vectors to work with later---
                if ngram in nouns_of_interest:
                    self.data.add((ngram, None))

                elif ngram_lemma in nouns_of_interest:
                    self.data.add((ngram_lemma, None))
                    
                else:
                    if token.text in nouns_of_interest:
                            self.data.add((token.text, None))

                    elif token_text_lemma in nouns_of_interest:
                        self.data.add((token_text_lemma, None))

                
                #---catch nouns of interest with whitespace---
                if last:
                    ngram = last + ' ' + token.text
        
                last = token.text
                possible_adj_nums = set()
                left = [token for token in dep[i].lefts]
                right = [token for token in dep[i].rights]
                possible_adj_nums = left + right
                
                #---add nouns of interest that occur with adjectives or numbers---
                for t in possible_adj_nums:

                    if t.tag_ in pos_tags:
                        adj_num = self.normalize_if_num(t.text)

                        if ngram in nouns_of_interest:
                            self.data.add((ngram, adj_num))

                        elif ngram_lemma in nouns_of_interest:
                            self.data.add((ngram_lemma, adj_num))
                            
                        else:
                            if token.text in nouns_of_interest:
                                self.data.add((token.text, adj_num))

                            elif token_text_lemma in nouns_of_interest:            
                                self.data.add((token_text_lemma, adj_num))
