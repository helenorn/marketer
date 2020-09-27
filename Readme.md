# Readme

## Libraries/packages 
### To run this program you need access to these libraries

### NLTK
I chose to use nltk because it is a popular library for natural language processing operations, especially when working with English language. It is my go-to for preprocessing data because of it's wide range of relevant functionaliy. In this case, I used the WordNetLemmatizer and sent_tokenize to prepare the documents for data extraction. For English, I prefer the nltk tokenizers, but If I were to process norwegian text, UDPIPE might be a better option because it is spesifically trained on both norwegian-bokmål and norwegian-nynorsk.

### Spacy
Since dependency parcing seemed like a good solution to this task, I chose to use spacy's dependency parcer. In my opinion, it's easy to use and has the functionality I need for this task. 

##### Download spacy support for english:
python -m spacy download en_core_web_sm

### Scikit-learn
I used scikit-learn because scikit-learn has many good tools for core natural language processing tasks, such as classification, regression, clustering and analyzation. In this case, I used the cosine_similarity function to compute the coisne similarity between the document vectors. I find scikit-learn more practical to use with less complex NLP tasks like this one, which does not need a lot of computing power. For more complex and demaning NLP tasks, libraries like Tensorflow and PyTorch might be a better fit. 

### matplotlib / seaborn
I used matplotlib / seaborn to plot a heatmap of the simiarity matrix. The matplotlib library is an extensive and easy-to-use library for data-visualization. Seaborn is based on matplotlib and adds some extra functionality, like heatmaps. 

### numpy
Numpy is a good library for working with arrays in python. I used numpy to present the similarity matrix as an array. 

## How to use
#### Initiate ExtractPropertyData
The ExtractPropertyData takes as input a txt-file with all the property descriptions. This file can contain any number of property descriptions, but each description must follow the property name on the form "Property n:" where n is the property number. Mistakes like additional whitespaces in the title are accounted for. 

Additionally, ExtractPropertyData takes as input the initial set of categories. Methods to add new nouns and categories are accounted for, but not implemented. 

#### extract, present_data
The extract method is called to extract the desiered data. 

#### add_nouns, update 
The methods add_nouns and update are not yet implemented, but accounted for. The idea is that the user can add new categories after the initial run, and get updated information about the documents. The update method can also be called after adding new property descriptions to the property txt-file. 

#### Initiate PropertySimilarityMatrix
get_matrix returns the matrix and plot_matrix plots a heatmap of the matrix

## Tests
### Run by calling testTechnicalChallenge.py with an argument
arg: extract or matrix
python testTechnicalChallenge.py arg

## Thoughts
###  Thoughts no one asked for, but no one was here to stop me either

#### Property names
If the property name is mentioned in the property description on the form "Property n:", there will be problems when splitting the document. Ideally, each property should have a unique property ID instead.


#### lemmatization
I noticed almost all the words in the provided category dictionart were lemmas, but wanted to make sure future non-lemmatized entries were accounted for as well. Consider the following tokens:

Receptions room
Reception room

Personally, I think keeping the entires on lemma-form will ensure that we capture as many similarities as possible, but to give the user flexibility for future special cases, the program will check for non-lemmatized nouns of interest in the property descrption first. If the non-lemmatized verison exists in the nouns of interest, we add the (noun, adj|num) touple to our data. Otherwise, we check the lemmatized version.


#### finding relevant nouns and adjectives
Let's get straight to the point: this program doesn't exactly perform perfectly. To every NLP task, there's a never ending stream of small tweaks and problems to solve before getting the optimal results (but that's the charm of it, innit?). 

Let's consider the following sentence from the description of property 5.

##### “A handsome and substantial six bedroom semi-detached Edwardian family house.

The desired results are:
bedroom: [ 'six' ]
house: ['handsome', 'substantial', 'semi-detached', 'edwardian', 'family']

The results, however, are...not quite there: 
bedroom : ['three', 'further', 'two', 'double', 'edwardian', 'detached', 'six']
house : ['six', 'detached', 'edwardian']

I initially implemented a version of the dependency parser that *only* found the correct dependency for house in this case (except the inclusion if 'six', but that is a minor issue compared to this one). I decided to search in the children of the local tree instead, as a temporary solution to acquiring more data. I reckon combination of both would be ideal. 

##### lost in tokenization?
It seems like spacy's tokenizer splits tokens on hyphens. Semi-detached becomes detatched, and its sad. One solution would be to modify spacy's tokenizer with new rules to handle special casses like this, but such modification can often lead to a butterfly-effect ending in other tokenization-problems. 

##### nouns
Since we don't have loads of data to work with, I decided to try to increase the number of vectors by adding nouns in the nouns of interest list to the data, even if they don't occur with with a adj|num. My theory is that property descriptions seldom list a lot of things the property doesn't have, therefore accounting for the noun itself might be favorable. This is just my theory though. The user can specify a penalty in range 0-1, to reduce the weight of the standalone noun. The default is set to 0.5. 
