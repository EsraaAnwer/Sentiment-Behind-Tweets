import re
import string
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords, webtext
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.isri import ISRIStemmer
from nltk.stem import WordNetLemmatizer 
from textblob import Word, TextBlob
from nlppreprocess import NLP



def one_string_lower_conversation(sentence):
    '''
    Argument:
        text as string of words
    return:
        lower of this string
    '''
    return sentence.lower()
  
def all_string_lower_conversation(text_list):
    '''
    Argument:
        list of strings and each of these strings does contain some of words
    return:
        lower each string in this list
    '''
    text_list = [one_string_lower_conversation(sentence) for sentence in text_list]
    return text_list


def one_string_remove_punctuation(sentence):
    '''
    Argument:
        string of words
    reutrn:
        string without punctuation like [.!?] and others
    '''
    sentence = re.sub("""(@\w+[1-9:'\/"]? |http:\/\/\w+.\w+.\w+\/)""", '', sentence)
    sentence = sentence.split(' ')
    
    strs = ''
    punctuations = string.punctuation
    for word in sentence:
        word = re.sub('[^\w\s+]',' ',word)
        strs += word + ' '
    translator = str.maketrans('', '', punctuations)
    strs.translate(translator)
    return strs

def all_strings_remove_punctuation(text_list):
    '''
    Argument:
        list of strings 
    reutrn:
        list of strings without punctuation like [.!?] and others
    '''
    text_list = [one_string_remove_punctuation(sentence) for sentence in text_list]
    return text_list


def one_string_tokenization(sentence):
    '''
    Argument:
        String of words
    return:
        list of words
    '''
    sentence = word_tokenize(sentence)
    return sentence


def all_string_tokenization(text_list):
    '''
    Argument:
        list of Strings
    return:
        list of strings and every string is list of words
    '''
    text_list = [one_string_tokenization(sentence) for sentence in text_list]
    return text_list


def one_string_Lemmatizing(sentence):
    '''
    Argument:
        String of words
    return:
        list of words with Lemmatizing
    '''
    sentence = one_string_tokenization(sentence)
    lemmatizer = WordNetLemmatizer()
    sentence = [lemmatizer.lemmatize(word) for word in sentence]
    return sentence

def all_string_Lemmatizing(text_list):
    '''
    Argument:
        list of strings
    return:
        list of strings with steming which the root of the word in each string
    '''
    text_list = [one_string_Lemmatizing(sentence) for sentence in text_list]
    return text_list


def one_string_stop_words(sentence):
    '''
    Argument:
        string of words
    return:
        remove stop words from this string like this, did
        but other words like not, no dont remove
	'''
    stop_words = NLP().stopword_list
    sentence = sentence.split(' ')
    updated_sentence = ''
    for word in sentence:
    	if word not in stop_words:
    		updated_sentence += word + ' '
    return updated_sentence






def all_string_stop_words(text_list):
  '''
  Argument:
      list of string
  return:
      list of string without stop words
  '''
      
  text_list = [one_string_stop_words(sentence) for sentence in text_list]
  return text_list

def one_string_un_tokenization(sentence):
    '''
    Argument:
        list of words
    return:
        string of words
    '''
    sentence = " ".join(sentence)
    return sentence
    
def all_string_un_tokenization(text_list):
    '''
    Argument:
        list of words
    return:
        string of words
    '''
    text_list = [one_string_un_tokenization(sentence) for sentence in text_list]
    return text_list

def english_pip_line(text_list):
    text_list = all_string_lower_conversation(text_list)
    text_list = all_strings_remove_punctuation(text_list)
    text_list = all_string_stop_words(text_list)
    return text_list

    
