#!env/bin/python
import sys
from word_utils import *

(global_words_frequency, global_words_per_file) = get_most_frequent_words(sys.argv[1:])

ten_most_frequent = global_words_frequency[:10]

print("Word\tOcurrences\tDocuments\t3 sentences containing the word")
for word, occurences in ten_most_frequent:
    sentences = []
    for file_name in global_words_per_file[word]:
        try:
            file = open(file_name, 'r')
            text = file.read()
            sentences += [sentence for sentence in get_sentences(text) if is_word_in_sentence(word,sentence)]
        except IOError:
            print "Error: File does not appear to exist."
        finally:
            file.close()

    sentences = sentences[:3]
    print(word + "\t " + str(occurences) + "\t"+ ", ".join(global_words_per_file[word]) + "\t" + ". ".join(sentences))
