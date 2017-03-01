#!env/bin/python
from hamcrest import *
import unittest
from word_utils import *

# One unit test per function, several cases per unit test

class GetSentencesTest(unittest.TestCase):
    def testSentencesSeparatedByDots(self):
        sentences = get_sentences("         one sentence. two sentences      ")
    	assert_that(sentences, has_length(2))
    	assert_that(sentences[0], equal_to("one sentence"))
    	assert_that(sentences[1], equal_to("two sentences"))

    def testSentencesSeparatedByQuestionMark(self):
        sentences = get_sentences("         one sentence? two sentences      ")
        assert_that(sentences, has_length(2))
        assert_that(sentences[0], equal_to("one sentence"))
        assert_that(sentences[1], equal_to("two sentences"))

    def testSentencesSeparatedByExclamationMark(self):
        sentences = get_sentences("         one sentence! two sentences      ")
        assert_that(sentences, has_length(2))
        assert_that(sentences[0], equal_to("one sentence"))
        assert_that(sentences[1], equal_to("two sentences"))

    def testSentencesSeparatedByDotsWithEmptySentences(self):
        sentences = get_sentences("         one sentence. two sentences.    .   .  .  . ....")
        assert_that(sentences, has_length(2))
        assert_that(sentences[0], equal_to("one sentence"))
        assert_that(sentences[1], equal_to("two sentences"))


class MergeDictionariesTest(unittest.TestCase):
    def testWithStringToIntegerDictionaries(self):
        result = merge_dictionaries({'a': 1, 'b': 1, 'c': 1}, {'a': 1, 'b': 1, 'e': 1})
        assert_that(result, equal_to({'a': 2, 'b': 2, 'c': 1, 'e':1}))

    def testWithStringToListDictionaries(self):
        result = merge_dictionaries({'a': [1], 'b': [2]}, {'a':[3], 'c':[1,2]})
        assert_that(result, equal_to({'a':[1,3], 'b':[2], 'c':[1,2]}))

class IsWordInSentenceTest(unittest.TestCase):
    def testWordPresentInSentence(self):
	    word_in_sentence = is_word_in_sentence("me", "Sentence containing the word me")
	    assert_that(word_in_sentence, is_(True))

    def testWordNotPresentInSentence(self):
	    word_in_sentence = is_word_in_sentence("me", "Sentence not containing the word")
	    assert_that(word_in_sentence, is_(False))

    def testIsCaseInsensitive(self):
	    word_in_sentence = is_word_in_sentence("me", "Sentence not containing the word ME")
	    assert_that(word_in_sentence, is_(True))

	    word_in_sentence = is_word_in_sentence("WORD", "Sentence not containing the word ME")
	    assert_that(word_in_sentence, is_(True))


class GetWordsFrecuancyTest(unittest.TestCase):
    def testEmptyString(self):
        result = get_words_frequency("")
        assert_that(result, equal_to({}))

    def testWhitSimpleSentence(self):
        result = get_words_frequency("pepe cat cat dog dog dog duck duck duck duck")
        assert_that(result, is_(equal_to({'pepe':1, 'cat':2, 'dog':3, 'duck':4})))

    def testWhitComplexSentences(self):
        result = get_words_frequency("pepe, cat, cat? Dog! dog! Dog. Duck??? duck!! duck... duck? .")
        assert_that(result, is_(equal_to({'pepe':1, 'cat':2, 'dog':3, 'duck':4})))

    def testWhitComplexSentencesAndStopWords(self):
        result = get_words_frequency("one information? Other     no about search. Search by this cat cat. No")
        assert_that(result, is_(equal_to({'cat':2})))


class GetMostFrequentWordsIntegrationTest(unittest.TestCase):
    def testEmptyFiles(self):
        (global_words_frequency, global_words_per_file)=get_most_frequent_words([])
        assert_that(global_words_frequency, equal_to([]))
        assert_that(global_words_per_file, equal_to({}))

    def testWithSimpleDocument(self):
        (global_words_frequency, global_words_per_file) = get_most_frequent_words(["./test-docs/test2.txt", "./test-docs/test3.txt"])
        assert_that(global_words_frequency, equal_to([('cat', 5), ('duck', 4), ('dog', 3), ('pepe', 1)]))
        assert_that(global_words_per_file, equal_to({'cat': ['./test-docs/test2.txt', './test-docs/test3.txt'], 'pepe': ['./test-docs/test2.txt'], 'dog': ['./test-docs/test2.txt', './test-docs/test3.txt'], 'duck': ['./test-docs/test2.txt', './test-docs/test3.txt']}))

    def testWithComplexDocument(self):
        (global_words_frequency, global_words_per_file) = get_most_frequent_words(["./test-docs/test3.txt", "./test-docs/test4.txt"])
        assert_that(global_words_frequency, equal_to([('duck', 7), ('cat', 7), ('dog', 5)]))
        assert_that(global_words_per_file, equal_to({'cat': ['./test-docs/test3.txt', './test-docs/test4.txt'], 'dog': ['./test-docs/test3.txt', './test-docs/test4.txt'], 'duck': ['./test-docs/test3.txt', './test-docs/test4.txt']}))

    def testWithComplextDocumentAndStopWords(self):
        (global_words_frequency, global_words_per_file) = get_most_frequent_words(["./test-docs/test1.txt", "./test-docs/test2.txt"])
        assert_that(global_words_frequency, equal_to([('dog', 5), ('cat', 5), ('duck', 1), ('dogs', 1), ('big', 1), ('level', 1), ('house', 1), ('main', 1), ('pepe', 1)]))
        assert_that(global_words_per_file, equal_to({'duck': ['./test-docs/test2.txt'], 'dogs': ['./test-docs/test1.txt'], 'big': ['./test-docs/test1.txt'], 'level': ['./test-docs/test1.txt'], 'house': ['./test-docs/test1.txt'], 'main': ['./test-docs/test1.txt'], 'pepe': ['./test-docs/test2.txt'], 'dog': ['./test-docs/test1.txt', './test-docs/test2.txt'], 'cat': ['./test-docs/test1.txt', './test-docs/test2.txt']}))

if __name__ == '__main__':
    unittest.main()
