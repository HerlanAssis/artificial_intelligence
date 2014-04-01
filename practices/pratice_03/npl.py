# -*- coding: utf-8 -*-
from nltk.tokenize import WordPunctTokenizer
import random, re

end_of_phrase = ['.','?','!']
punctuations = [';',',',':']
end_of_word = punctuations + end_of_phrase

def bag_of_words(file_name):
    return WordPunctTokenizer().tokenize(open(file_name).read().lower())  

def make_n_gram(n, words):
    n_grams = [words[i:i+n] for i in range(len(words)-n+1)]
    return n_grams

def words_sequence_map(n_grams):
    dict = {}
    for n_gram in n_grams:        
        key = '_'.join(n_gram[0:-1])
        if not(dict.has_key(key)):
            dict[key] = []
        dict[key].append(n_gram[-1])
    return dict

def unigram_next_word(words):
    return random.choice(words)

def n_gram_next_word(key_words_sequence, _words_sequence_map):    
    dict = _words_sequence_map
    key = '_'.join(key_words_sequence[0:-1])
    return random.choice(dict[key]) if dict.has_key(key) else None

def make_phrase(n, n_grams, words, _words_sequence_map):
    phrase = ''
    last_word = None
    if n == 1:        
        while True:
            word = unigram_next_word(words)
            if (last_word != None and word == last_word) or (last_word == None and not(word.isalpha())): continue
            phrase += ' ' + word if not(word in end_of_word) else word
            if word in end_of_phrase: break
            last_word = word             
    else:
        key_words_sequence = random.choice(n_grams)
        words_sequence = []
        while True:            
            word = n_gram_next_word(key_words_sequence, _words_sequence_map)            
            if word == None: continue
            last_n_gram = words_sequence[-n+2:]+[word] if -n+2 or len(words_sequence) + 1 < n-1 else [word]                
            if len(words_sequence) + 1 < n-1:
                word_n_grams = [n_gram for n_gram in n_grams if n_gram[-2] == last_n_gram[-1]]
            else:                                
                word_n_grams = [n_gram for n_gram in n_grams if n_gram[:len(last_n_gram)] == last_n_gram]                                                                                                    
            if not(len(word_n_grams)) and not(word in end_of_phrase) or (last_word != None and word == last_word) or (last_word == None and not(word.isalpha())):
                key_words_sequence = random.choice(n_grams)
                continue                
            phrase += ' ' + word if not(word in end_of_word) else word
            if word in end_of_phrase: break                
            key_words_sequence = random.choice(word_n_grams)            
            words_sequence.append(word)
            last_word = word
    return phrase[1:].capitalize()

def main():
    words = bag_of_words('bag_of_words.txt')    
    n = 3
    n_grams = make_n_gram(n, words)        
    _words_sequence_map = words_sequence_map(n_grams)
    print 'Markov N-gram generation - Artificial Inteligence - João Helis\n'
    for count in range(5):
        print 'N'+str(n)+': ' + make_phrase(n, n_grams, words, _words_sequence_map)
    
main()