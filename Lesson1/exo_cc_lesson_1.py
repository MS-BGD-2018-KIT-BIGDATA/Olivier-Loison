import unittest
# zip, map , lamba (zip: return un table de tupple Ã  partir de 2 tableaux)
# set : list unique avec intersec, diff , union
# test unitaires dans le main avec des contrats tres simples (les 'ok') module unittest
# TDD test driven developpement si on doit ecrire un programmme on commencepar ecrire les tests
# TDD pour gerer aussi les erreurs
# BDD behavior driven dev , test nton integration : user facing (regroupe les TDD, comme un tuto)

# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    return string*n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    #longueur=min(len(nums) & 4)
    for i in range(len(nums)):
        if  i<4 and nums[i] == 9:
            return True
    return False

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    pattern = string[-2:]
    cpt = 0
    for i in range(0, len(string)-3):
        if string[i:i+2] == pattern:
            cpt += 1
    return cpt


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.


def length_words(array):
    # on peut aussi faire une liste comprÃ©hension
    return [i.length for i in array]

#write fizbuzz programm
def fizbuzz():
    return(['Fizz'*(i%3<1)+'Buzz'*(i%5<1) or i for i in range(1,11)])

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
  return [x for x in str(number)]  

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
  return ' '.join([x[1:]+x[0]+'ay' for x in text.split()]).capitalize()

#Write a proramm that returna dictionary of occurences of the alphabet for a given string.
# Test it with the Lorem upsuj
#"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
def occurences(text):
      result = {}
      for x in text:
          if x not in result:
              result[x] = 1
          else:
              result[x] +=1
      return result

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    fizbuzz()
    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")
