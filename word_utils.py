import re
import string

def get_most_frequent_words(file_names=[]):
    global_words_frequency = {}
    global_words_per_file = {}

    for file_name in file_names:
        try:
            file = open(file_name, 'r')
            text = file.read()

            words_frequency = get_words_frequency(text)
            global_words_frequency = merge_dictionaries(global_words_frequency, words_frequency)

            words_per_file = dict( (i, [file_name]) for i in words_frequency.keys())
            global_words_per_file = merge_dictionaries(global_words_per_file, words_per_file)

            sentences = get_sentences(text)
        except IOError:
            print "Error: File does not appear to exist."
        finally:
            file.close()

    global_words_frequency = list(global_words_frequency.iteritems())
    global_words_frequency.sort(key=lambda tup: tup[1], reverse=True)

    return (global_words_frequency, global_words_per_file)


def get_words_frequency(text = ""):
    # For simplicity's shake, stops words are hardcoded
    stop_words = ["the", "of", "and", "to", "a", "in", "for", "is", "on","that",\
    "by","this","with","i","you","it","not","or","be","are","from","at","as","your",\
    "all","have","new","more","an","was","we","will","home","can","us","about","if",\
    "page","my","has","search","free","but","our","one","other","do","no","information","time"]
    words = {}
    sentences = get_sentences(text)

    for sentence in sentences:
        sentence_words = [word.strip(string.punctuation) for word in sentence.split()]
        for word in sentence_words:
            if len(word) > 0:
                to_lower = word.lower()
                if  words.has_key(to_lower):
                    words[to_lower] = words[to_lower] + 1
                else:
                    words[to_lower] = 1

    # Remove stop words
    for stop_word in stop_words:
        if words.has_key(stop_word):
            words.pop(stop_word)

    return words

def get_sentences(text=""):
    return [sentence.strip() for sentence in re.split(r' *[\.\?!][\'"\)\]]* *', text) if len(sentence) > 0]

def is_word_in_sentence(word, sentence):
    return word.lower() in sentence.lower().split()

def merge_dictionaries(d1, d2):
    result = dict(d1)
    for k,v in d2.iteritems():
        if k in result:
            result[k] = result[k] + v
        else:
            result[k] = v
    return result
