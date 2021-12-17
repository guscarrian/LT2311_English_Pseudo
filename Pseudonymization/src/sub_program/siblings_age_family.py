# Modules
import nltk
import re, random
import pandas as pd
import numpy as np
from Levenshtein import distance
import argparse

# If it is misspelled then the function corrects the spelling and then randomly change to a digit
def get_correct_spelling(word, list_number):
  return min(list_number, key=lambda x: distance(word, x))

# Randomly change the age of a person given in the text
def age(filename, dict_numbers):
  temp_list = []
  for x in data:
    if re.search(r'\är \d{2} ', x):
      y = re.findall(r'\d{2}', x)
      y1 = str(int(y[0]) + random.randint(-2,2))
      z = x.split(' ')
      for i, j in enumerate(z):
        if j == y[0]:
          z[i] = y1
      temp_list.append(' '.join(z))
    elif len(re.findall(r'(fylla|fyller|fyllde|fyllt) (\d{2}) ', x)) > 0:
      y = re.findall(r'\d{2}', x)
      y1 = str(int(y[0]) + random.randint(-2,2))
      z = x.split(' ')
      for i, j in enumerate(z):
        if j == y[0]:
          z[i] = y1
      temp_list.append(' '.join(z))
    elif len(re.findall(r'(fylla|fyller|fyllde|fyllt) (\w+) ', x)) > 0:
      list_number = tuple([key for key, value in dict_numbers.items()])
      y = re.findall(r'(fylla|fyller|fyllde|fyllt) (\w+) ', x)
      y1 = list(y[0])
      y2 = get_correct_spelling(y1[1], list_number)
      y3 = dict_numbers[y2]
      y3 = str(int(y3) + random.randint(-2,2))
      z = x.split(' ')
      for i, j in enumerate(z):
        if j == y1[1]:
          z[i] = y3
      temp_list.append(' '.join(z))
    else:
      temp_list.append(x)
  return(temp_list)

# Function to change the information of the family members
def family_shift(data, list_family):
  temp_list = []
  for x in data:
    y = x.split(' ')
    for i, j in enumerate(y):
      for k in list_family:
        if j == k:
          y[i] = random.choice(list_family)
    temp_list.append(' '.join(y))
  return(temp_list)

# Randomly change the information about the number of siblings and friends in the text
def siblings(data, list_siblings):
  temp_list = []
  for x in data:
    if re.search(r'kompisar', x):
      y = re.findall(r' ([\w]+) kompisar', x)
      z = x.split(' ')
      for i, j in enumerate(z):
        if j == y[0]:
          z[i] = random.choice(list_siblings)
      temp_list.append(' '.join(z))
    elif re.search(r'bröder', x):
      y = re.findall(r' ([\w]+) bröder', x)    #brothers (plural?)
      z = x.split(' ')
      for i, j in enumerate(z):
        if j == y[0]:
          z[i] = random.choice(list_siblings)
      temp_list.append(' '.join(z))
    elif re.search(r'systern', x):              #systern --> singular bestämd form?? --> systrar?pl
      y = re.findall(r' ([\w]+) systern', x)
      z = x.split(' ')
      for i, j in enumerate(z):
        if j == y[0]:
          z[i] = random.choice(list_siblings)
      temp_list.append(' '.join(z))
    else:
      temp_list.append(x)
  return(' '.join(temp_list))

if __name__ == '__main__':
  
  #dict_numbers = {'arton': '18','elva': '11','en': '1','fem': '5','femtio': '50','femtioen': '51','femtiofem': '55','femtiofyra': '54','femtionio': '59','femtiosex': '56','femtiosju': '57','femtiotre': '53','femtiotvå': '52','femtioåtta': '58','femton': '15','fjorton': '14','fyra': '4','fyrtio': '40','fyrtioen': '41','fyrtiofem': '45','fyrtiofyra': '44','fyrtionio': '49','fyrtiosex': '46','fyrtiosju': '47','fyrtiotre': '43','fyrtiotvå': '42','fyrtioåtta': '48','hundra': '100','nio': '9','nittio': '90','nittioen': '91','nittiofem': '95','nittiofyra': '94','nittionio': '99','nittiosex': '96','nittiosju': '97','nittiotre': '93','nittiotvå': '92','nittioåtta': '98','nitton': '19','sex': '6','sextio': '60','sextioen': '61','sextiofem': '65','sextiofyra': '64','sextionio': '69','sextiosex': '66','sextiosju': '67','sextiotre': '63','sextiotvå': '62','sextioåtta': '68','sexton': '16','sju': '7','sjuttio': '70','sjuttioen': '71','sjuttiofem': '75','sjuttiofyra': '74','sjuttionio': '79','sjuttiosex': '76','sjuttiosju': '77','sjuttiotre': '73','sjuttiotvå': '72','sjuttioåtta': '78','sjutton': '17','tio': '10','tjugo': '20','tjugoen': '21','tjugofem': '25','tjugofyra': '24','tjugonio': '29','tjugosex': '26','tjugosju': '27','tjugotre': '23','tjugotvå': '22','tjugoåtta': '28','tolv': '12','tre': '3','trettio': '30','trettioen': '31','trettiofem': '35','trettiofyra': '34','trettionio': '39','trettiosex': '36','trettiosju': '37','trettiotre': '33','trettiotvå': '32','trettioåtta': '38','tretton': '13','två': '2','åtta': '8','åttio': '80','åttioen': '81','åttiofem': '85','åttiofyra': '84','åttionio': '89','åttiosex': '86','åttiosju': '87','åttiotre': '83','åttiotvå': '82','åttioåtta': '88'}
    
    dict_numbers = {'eighteen': '18','eleven': '11','one': '1','five': '5','fifty': '50','fifty-one': '51','fifty-five': '55','fifty-four': '54','fifity-nine': '59','fifty-six': '56','fifty-seven': '57','fifty-three': '53','fifty-two': '52','fifty-eight': '58','fifteen': '15','fourteen': '14','four': '4','forty': '40','forty-one': '41','forty-five': '45','forty-four': '44','forty-nine': '49','forty-six': '46','forty-seven': '47','forty-three': '43','forty-two': '42','forty-eight': '48','one hundred': '100','nine': '9','ninety': '90','ninety-one': '91','ninety-five': '95','ninety-four': '94','ninety-nine': '99','ninety-six': '96','ninety-seven': '97','ninety-three': '93','ninety-two': '92','ninety-eight': '98','nineteen': '19','six': '6','sixty': '60','sixty-one': '61','sixty-five': '65','sixty-four': '64','sixty-nine': '69','sixty-six': '66','sixty-seven': '67','sixty-three': '63','sixty-two': '62','sixty-eight': '68','sixteen': '16','seven': '7','seventy': '70','seventy-one': '71','seventy-five': '75','seventy-four': '74','seventy-nine': '79','seventy-six': '76','seventy-seven': '77','seventy-three': '73','seventy-two': '72','seventy-eight': '78','seventeen': '17','ten': '10','twenty': '20','twenty-one': '21','twenty-five': '25','twenty-four': '24','twenty-nine': '29','twenty-six': '26','twenty-seven': '27','twenty-three': '23','twenty-two': '22','twenty-eight': '28','twelve': '12','three': '3','thirty': '30','thirty-one': '31','thirty-five': '35','thirty-four': '34','thirty-nine': '39','thirty-six': '36','thirty-seven': '37','thirty-three': '33','thirty-two': '32','thirty-eight': '38','thirteen': '13','two': '2','eight': '8','eighty': '80','eighty-one': '81','eighty-five': '85','eighty-four': '84','eighty-nine': '89','eighty-six': '86','eighty-seven': '87','eighty-three': '83','eighty-two': '82','eighty-eight': '88'}
  
  #list_family = ['kompis', 'sambo','föräldrar','far','pappa','mamma','mor','barn','son','dotter','fru','bror','syster','farbror','morbror','faster','moster','kusin','brorson','systerson','nevö','brorsdotter','systerdotter','farföräldar','morföräldar','farfar','morfar','farmor','mormor','barnbarn','sonson','sondotter','svärfar','svärmor','svåger','svägerska']
  
  list_family = ['partner?', 'cohabitant', 'parents',' father ',' dad ',' mother ',' mum ',' child ',' son ',' daughter ',' wife ',' brother ',' sister ',' uncle ',' aunt ',' cousin ',' nephew ',' niece ', 'grandparents' , 'grandfather', 'grandmother', 'granddaughter', 'grandson', 'father-in-law', 'mother-in-law', 'brother-in-law', 'sister-in-law']

  #list_siblings = ['två', 'tre', 'fyra', 'fem', 'sex', 'sju']

  list_siblings = ['two', 'three', 'four', 'five', 'six', 'seven']


  parser = argparse.ArgumentParser(description='Program takes an input text file and output text file')
  
  parser.add_argument('--input', '-i', type=str, required=True)
  parser.add_argument('--output', '-o', type=str, required=True)
  args = parser.parse_args()
  
  # Read a given file and save the tokenized sentence data in a list
  with open(args.input) as file:
    data = file.read()

  data = re.sub(r'\n\n', ' $$$$ . ', data)
  data = nltk.sent_tokenize(data)
  data = age(data, dict_numbers)
  data = family_shift(data, list_family)
  data = siblings(data, list_siblings)
  data = data.replace(' $$$$ . ', '\n\n')

  if args.output:
    file = open(args.output, 'w')
    file.write(data)

