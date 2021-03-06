# Modules
import nltk
import re, random
import pandas as pd
import numpy as np
from Levenshtein import distance
import argparse, json
from os.path import abspath, dirname

MODULEDIR = dirname(dirname(abspath(__file__)))

# If it is misspelled then the function corrects the spelling and then randomly change to a digit
def get_correct_spelling(word, list_number):
    return min(list_number, key=lambda x: distance(word, x))


# Read list and dict from dict_data 
# File contains university names, relationship in family, days, months etc.
with open(MODULEDIR + '/dataset/dict_data.json', 'r') as file:
    dict_data = json.load(file)
    
dict_numbers = dict_data['dict_numbers']
list_family = dict_data['list_family']
list_siblings = dict_data['list_siblings']
list_days = dict_data['list_days']
list_months = dict_data['list_months']
dict_universities = dict_data['dict_universities']
list_transports = dict_data['list_transports']
list_stations = dict_data['list_stations']
list_stations_en = dict_data['list_stations_en']

with open(MODULEDIR + '/dataset/names_database.json', 'r') as file:
        dict_names = json.load(file)
       

    
list_job_title = pd.read_csv(MODULEDIR + '/dataset/Prof_dataset.csv')
list_data = pd.read_csv(MODULEDIR + '/dataset/city_country.csv')
list_swedish_cities = pd.read_csv(MODULEDIR + '/dataset/cities_sweden.csv')
list_swedish_island = pd.read_csv(MODULEDIR + '/dataset/island_sweden.csv')

# Main function to de-identify all the personal information and save as a text file
def identify(data):
    # To have the output format same as the input especially for newline and paragraphs in the text
    data = re.sub(r'\n\n', ' $$$$ . ', data)  
    data = nltk.sent_tokenize(data) # Sentence Tokenize to keep track on the 
    '''
    ##########
    # In this function a list of personal data is anonymised
    # Anonymise the vehicle registeration number (only Swedish)
    # Phone number - mobile, landline (only Swedish)
    # Date formats that are mostly used in various parts of the world
    # - 1111/11/11
    # - 11/11/11
    # - 111111
    # - 11.11.11
    # - 11/11
    # Personel Number format (only Swedish)
    # - 123456-0000
    # - 19123456-0000
    # - 1234560000
    # - 191234560000
    # Bank format in Sweden
    # - 1234-00 200 00
    # - 1234-123 123 123
    # - 1234-1 123 123 1234
    # Email addresses are changed to 'email@dot.com'
    # Website and URL are changed to "url.com" except person website
    # Person website is complicated to anonymise because there are thousands of domain to look for
    # - "personname.xx"
    ##########
    '''
    
    _data = []
    
    # Swedish bank account format
    for line in data:
        if re.search(r' \d{4}-\d{2} \d{3} \d{2} ', line):
            line = re.sub(r'(\d{4}-\d{2} \d{3} \d{2} )', '<bank_acc>0000-00 000 00</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{4}-\d{3} \d{3} \d{3} ', line):
            line = re.sub(r'(\d{4}-\d{3} \d{3} \d{3} )', '<bank_acc>0000-000 000 000</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{4}-\d{1} \d{3} \d{3} \d{4} ', line):
            line = re.sub(r'(\d{4}-\d{1} \d{3} \d{3} \d{4} )', '<bank_acc>0000-0 000 000 0000</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{4} \d{2} \d{3} \d{2} ', line):
            line = re.sub(r'(\d{4} \d{2} \d{3} \d{2} )', '<bank_acc>0000 00 000 00</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{4} \d{3} \d{3} \d{3} ', line):
            line = re.sub(r'(\d{4} \d{3} \d{3} \d{3} )', '<bank_acc>0000 000 000 000</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{4} \d{1} \d{3} \d{3} \d{4} ', line):
            line = re.sub(r'(\d{4} \d{1} \d{3} \d{3} \d{4} )', '<bank_acc>0000 0 000 000 0000</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{11} ', line):
            line = re.sub(r'(\d{11} )', '<bank_acc>00000000000</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{13} \d{1} \d{3} \d{3} \d{4} ', line):
            line = re.sub(r'(\d{13} )', '<bank_acc>0000000000000</bank_acc> ', line)
            _data.append(line)
        elif re.search(r' \d{15} \d{1} \d{3} \d{3} \d{4} ', line):
            line = re.sub(r'(\d{15} )', '<bank_acc>000000000000000</bank_acc> ', line)
            _data.append(line)
        else:
            _data.append(line)
    
    data = _data
    _data = []
    
    for line in data:
        if re.search(r' [A-Za-z]{3} \d{3} ', line):  # Vehicle License number
            line = re.sub(r'(\w{3} \d{3})', '<license_nr>ABC 000</license_nr> ', line)
        if re.search(r' \d{3}-\d{6} ', line):  # Landline number in Sweden
            line = re.sub(r'(\d{3}-\d{6})', '<landline_nr>000-000000</landline_nr> ', line)
        if 'mobil' in line:  # Mobile number format
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if re.search('\d{10}', j):
                    line_split[i] = '<mobile_nr>0000-000000</mobile_nr>'
            _data.append(' '.join(line_split))
        else:
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                #1111-11-11 //// 1111/11/11 //// 1111.11.11
                if re.search(r'^\d{4}-\d{2}-\d{2}$', j):  # Date 1111-11-11
                    line_split[i] = '<date_type>1111-11-11</date_type>'
                if re.search(r'^\d{4}\/\d{2}\/\d{2}$', j):  # TESTING 1111/11/11
                    line_split[i] = '<date_type>1111/11/11</date_type>'     
                if re.search(r'^\d{4}.\d{2}.\d{2}$', j):  # Date 1111.11.11 ---- NEW
                    line_split[i] = '<date_type>1111.11.11</date_type>'
                #11-11-1111 //// 11/11/1111 //// 11.11.1111   
                if re.search(r'^\d{2}\-\d{2}\-\d{4}$', j):  # Date 11-11-1111 ---- NEW: as in mm-dd-yyyy and dd-mm-yyyy
                    line_split[i] = '<date_type>11-11-1111</date_type>'
                if re.search(r'^\d{2}\/\d{2}\/\d{4}$', j):  # Date 11/11/1111 ---- NEW: as in mm/dd/yyyy and dd/mm/yyyy
                    line_split[i] = '<date_type>11/11/1111</date_type>'    
                if re.search(r'^\d{2}\.\d{2}\.\d{4}$', j):  # Date 11.11.1111 ---- NEW: as in mm.dd.yyyy and dd.mm.yyyy
                    line_split[i] = '<date_type>11.11.1111</date_type>'  
                #11-11-11 //// 11/11/11 //// 11.11.11
                if re.search(r'^\d{2}\-\d{2}\-\d{2}$', j):  # Date 11-11-11 ---- ENG SAME mm-dd-yy and dd-mm-yy
                    line_split[i] = '<date_type>11-11-11</date_type>'
                if re.search(r'^\d{2}\/\d{2}\/\d{2}$', j):  # Date 11/11/11 ---- ENG SAME mm/dd/yy and dd/mm/yy
                    line_split[i] = '<date_type>11/11/11</date_type>'
                #11-11 //// 11/11 //// 11.11
                #if re.search(r'^\d{1,2}/\d{2}$', j):  # Date 11/11
                    #line_split[i] = '<date_type>11/11<date_type>'
                if re.search(r'^\d{6}$', j) or re.search(r'^\d{8}$', j):  # Date 111111
                    line_split[i] = '<date_type>111111</date_type>'
                #if re.search(r'^\d{2}\.\d{2}\.\d{2}$', j):  # Date 11.11.11
                    #line_split[i] = '<date_type>11.11.11</date_type>'
                if re.search(r'^\d{4}$', j):  # Year - randomise "2018" with (-2,2) # If statement
                    line_split[i] = '<year_type>'+str(int(j) + random.randint(-2,2))+'</year_type>'
                # Personal number formats
                if re.search('\d{6}-\d{4}', j) or re.search('\d{8}-\d{4}', j) or re.search('\d{10}',j) or re.search('\d{12}', j):
                    line_split[i] = '<personal_id>123456-0000</personal_id>'
                if '@' in j:  # Email addresses are formatted to email @dot.com
                    line_split[i] = '<email_address>email@dot.com</email_address>'
                if 'https' in j:  # https url format
                    line_split[i] = '<url_link>url.com</url_link>'
                if 'http' in j: # http url format
                    line_split[i] = '<url_link>url.com</url_link>'
                if 'www' in j:  # www web address
                    line_split[i] = '<url_link>url.com</url_link>'
            _data.append(' '.join(line_split))
            
    data = _data
    _data = []
           
    # Randomised days in the data using a list of all the days in a week
    for line in data:
        line_split = line.split(' ')
        for i, j in enumerate(line_split):
            for k in list_days:
                if j == k:
                    line_split[i] = '<day_type>'+random.choice(list_days)+'</day_type>'
        _data.append(' '.join(line_split))
    data = _data
    _data = []
    
    # Randomised months loop
    for line in data:
        line_split = line.split(' ')
        for i, j in enumerate(line_split):
            for k in list_months:
                if j == k:
                    line_split[i] = '<month_type>'+random.choice(list_months)+'</month_type>'
        _data.append(' '.join(line_split))
     
    data = _data
    _data = []
    
    for line in data:
        if re.search(r'\??r \d{2} ', line): # Age mentioned in numbers are randomised with (-2,2)
            y = re.findall(r'\??r (\d{2}) ', line)
            y1 = str(int(y[0]) + random.randint(-2,2))
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if j == y[0]:
                    line_split[i] = '<age_digit>'+y1+'</age_digit>'
            _data.append(' '.join(line_split))
        elif len(re.findall(r'(fylla|fyller|fyllde|fyllt) (\d{2}) ', line)) > 0: 
            # Age mentioned in numbers are randomised with (-2,2) using RegEx
            y = re.findall(r'\d{2}', line)
            y1 = str(int(y[0]) + random.randint(-2,2))
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if j == y[0]:
                    line_split[i] = '<age_digit>'+y1+'</age_digit>'
            _data.append(' '.join(line_split))
        elif len(re.findall(r'(fylla|fyller|fyllde|fyllt) (\w+) ', line)) > 0:
            # Age mentioned in words are randomised with (-2,2)
            # If the age is misspelled then it is autocorrected and then randomised
            list_number = tuple([key for key, value in dict_numbers.items()])
            y = re.findall(r'(fylla|fyller|fyllde|fyllt) (\w+) ', line)
            y1 = list(y[0])
            y2 = get_correct_spelling(y1[1], list_number)
            y3 = dict_numbers[y2]
            y3 = str(int(y3) + random.randint(-2,2))
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if j == y1[1]:
                    line_split[i] = '<age_string>'+y3+'</age_string>'
            _data.append(' '.join(line_split))
        else:
            _data.append(line)
            
    data = _data
    _data = []
    
    for line in data:
        line_split = line.split(' ')
        for i, j in enumerate(line_split):
            for k in list_family:
                if j == k:
                    line_split[i] = '<family_info>'+random.choice(list_family)+'</family_info>'
        _data.append(' '.join(line_split))
    
    data = _data
    _data = []
    
    for line in data:
        if re.search(r'kompisar', line):
            y = re.findall(r' ([\w]+) kompisar', line)
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if j == y[0]:
                    line_split[i] = '<family_info>'+random.choice(list_siblings)+'</family_info>'
            _data.append(' '.join(line_split))
        elif re.search(r'br??der', line):
            y = re.findall(r' ([\w]+) br??der', line)
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if j == y[0]:
                    line_split[i] = '<family_info>'+random.choice(list_siblings)+'</family_info>'
            _data.append(' '.join(line_split))
        elif re.search(r'systern', line):
            y = re.findall(r' ([\w]+) systern', line)
            line_split = line.split(' ')
            for i, j in enumerate(line_split):
                if j == y[0]:
                    line_split[i] = '<family_info>'+random.choice(list_siblings)+'</family_info>'
            _data.append(' '.join(line_split))
        else:
            _data.append(line)
            
    data = _data
    _data = []
    
    
    for line in data:
        for y,z in dict_universities.items():
            for i in z:
                if i in line:
                    new_name = random.choice(list(dict_universities.keys()))
                    line = line.replace(i, '<university_name>'+dict_universities[new_name][0]+'</university_name>')   
                    break
            break
        _data.append(line)
                
    data = _data
    _list = []
    _data = []
    
    list_title = list_job_title['Yrkesben??mning'].tolist()
    list_title = list_title[:-7]
    
    for x in list_title:
        if ',' in x:
            y = x.split(',')
            _list.append(y[0].lower())
        else:
            _list.append(x.lower())
            
    for line in data:
        for y in _list:
            if y in line.split(' '):
                line = line.replace(y, '<prof_id>'+random.choice(_list)+'</prof_id>')
        _data.append(line)

        
    data = _data
    country_in_data = {}
    cities_in_data = {}
    
    list_country = list_data['Countries'].tolist()
    list_city = list_data['Cities'].tolist()
    
    for i in data:
        for j in set(list_country):
            if str(j) in i:
                country_in_data[list_country.index(str(j))] = j
        for k in set(list_city):
            if k in i.split(' '):
                cities_in_data[list_city.index(k)] = k
                
    _data = ' '.join(data)
    
    if len(country_in_data) > 0:
        if len(cities_in_data) > 0:
            for i,j in cities_in_data.items():
                index = list_city.index(j)
                if list_country[index] in country_in_data.values():
                    x = random.choice(list_country)
                    _data = _data.replace(list_country[index], '<country_name>'+x+'</country_name>')
                    _index = list_country.index(x)
                    _data = _data.replace(list_city[index], '<city_name>'+list_city[_index]+'</city_name>')
                else:
                    _data = _data.replace(j, '<city_name>'+random.choice(list_city)+'</city_name>')
            for i,j in country_in_data.items():
                index = list_country.index(j)
                if list_city[index] in cities_in_data.values():
                    x = random.choice(list_city)
                    _data = _data.replace(list_city[index], '<city_name>'+x+'</city_name>')
                    _index = list_city.index(x)
                    _data = _data.replace(list_country[index], '<country_name>'+list_country[_index]+'</country_name>')
                else:
                    _data = _data.replace(j, '<country_name>'+random.choice(list_country)+'</country_name>')
    elif len(cities_in_data) > 0:
        for i,j in cities_in_data.items():
            _data = _data.replace(j, '<city_name>'+random.choice(list_city)+'</city_name>')
            
    data = nltk.sent_tokenize(_data)  
    _data = []

    list_cities = list_swedish_cities['Cities'].tolist()
    
    for line in data:  # Cities
        line_split = line.split(' ')
        for i, j in enumerate(line_split):
            for k in list_cities:
                if j == k:
                    line_split[i] = '<swedish_city>'+random.choice(list_cities)+'</swedish_city>'
        _data.append(' '.join(line_split))
        
    data = _data
    _data = []
    list_cities = list_swedish_island['Island'].tolist()
    
    for line in data:  # Island
        line_split = line.split(' ')
        for i, j in enumerate(line_split):
            for k in list_cities:
                if j == k:
                    line_split[i] = '<swedish_island>'+random.choice(list_cities)+'</swedish_island>'
        _data.append(' '.join(line_split))
        
    data = _data
    _data = []
    
    for line in data:  # Postal Code only swedish
        if re.search(r' \d{3} \d{2} ', line):
            line = re.sub(r'(\d{3} \d{2})', '<postal_code>000 00</postal_code>', line)
            _data.append(line)
        else:
            _data.append(line)

    data = _data
   
    dict_tilltal_man = {}
    dict_tilltal_kvn = {}
    dict_fornamn_man = {}
    dict_fornamn_kvn = {}
    dict_efternamn = {}

    for line in data:
        for i in range(len(dict_names['tilltal_m??n'][0])):
            if dict_names['tilltal_m??n'][0][i] in line.split(' '):
                if i not in dict_tilltal_man:
                    dict_tilltal_man[i] = (len(dict_tilltal_man.keys())+1, 
                                           dict_names['tilltal_m??n'][0][i],
                                           random.choice(dict_names['tilltal_m??n'][0]),
                                           random.choice(dict_names['tilltal_m??n'][0]),
                                           random.choice(dict_names['tilltal_m??n'][0])
                                          )
                else:
                    pass
        for i in range(len(dict_names['f??rnamn_m??n'][0])):
            if dict_names['f??rnamn_m??n'][0][i] in line.split(' '):
                if i not in dict_fornamn_man:
                    dict_fornamn_man[i] = (len(dict_fornamn_man.keys())+1,
                                           dict_names['f??rnamn_m??n'][0][i],
                                           random.choice(dict_names['f??rnamn_m??n'][0]),
                                           random.choice(dict_names['f??rnamn_m??n'][0]),
                                           random.choice(dict_names['f??rnamn_m??n'][0]),
                                           random.choice(dict_names['efternamn'][0]),
                                           random.choice(dict_names['efternamn'][0]),
                                           random.choice(dict_names['efternamn'][0])
                                          )
                else:
                    pass
        for i in range(len(dict_names['efternamn'][0])):
            if dict_names['efternamn'][0][i] in line.split(' '):
                if i not in dict_efternamn:
                    dict_efternamn[i] = (len(dict_efternamn.keys())+1,
                                         dict_names['efternamn'][0][i],
                                         random.choice(dict_names['efternamn'][0]),
                                         random.choice(dict_names['efternamn'][0]),
                                         random.choice(dict_names['efternamn'][0])
                                        )
                else:
                    pass
        for i in range(len(dict_names['tilltal_kvinnor'][0])):
            if dict_names['tilltal_kvinnor'][0][i] in line.split(' '):
                if i not in dict_tilltal_kvn:
                    dict_tilltal_kvn[i] = (len(dict_tilltal_kvn.keys())+1,
                                           dict_names['tilltal_kvinnor'][0][i],
                                           random.choice(dict_names['tilltal_kvinnor'][0]),
                                           random.choice(dict_names['tilltal_kvinnor'][0]),
                                           random.choice(dict_names['tilltal_kvinnor'][0])
                                          )
                else:
                    pass
        for i in range(len(dict_names['f??rnamn_kvinnor'][0])):
            if dict_names['f??rnamn_kvinnor'][0][i] in line.split(' '):
                if i not in dict_fornamn_kvn:
                    dict_fornamn_kvn[i] = (len(dict_fornamn_kvn.keys())+1,
                                           dict_names['f??rnamn_kvinnor'][0][i],
                                           random.choice(dict_names['f??rnamn_kvinnor'][0]),
                                           random.choice(dict_names['f??rnamn_kvinnor'][0]),
                                           random.choice(dict_names['f??rnamn_kvinnor'][0]),
                                           random.choice(dict_names['efternamn'][0]),
                                           random.choice(dict_names['efternamn'][0]),
                                           random.choice(dict_names['efternamn'][0])
                                          )
                else:
                    pass


    _data = ' '.join(data)
    data = _data.split(' ')

    for i,j in enumerate(data):
        for key,value in dict_fornamn_man.items():
            if value[1] == j:
                if data[i-1] in dict_names['f??rnamn_m??n'][0]:
                    data[i-1] = '<fornamn_man>'+str(value[3])+'</fornamn_man>'
                    data[i] = '<fornamn_man>'+str(value[2])+'</fornamn_man>'
                    if data[i+1] in dict_names['efternamn'][0]:
                        data[i+1] = '<efternamn>'+str(value[5])+'</efternamn>'
                    if data[i+1] in dict_names['f??rnamn_man'][0]:
                        data[i+1] = '<fornamn_man>'+str(value[4])+'</fornamn_man>'
                        if data[i+2] in dict_names['efternamn'][0]:
                            data[i+2] = '<efternamn>'+str(value[5])+'</efternamn>'                
                elif data[i-1] not in dict_names['f??rnamn_m??n'][0]:
                    if data[i+1] in dict_names['f??rnamn_m??n'][0]:
                        data[i] = '<fornamn_man>'+str(value[2])+'</fornamn_man>'
                        data[i+1] = '<fornamn_man>'+str(value[4])+'</fornamn_man>'
                        if data[i+2] in dict_names['efternamn'][0]:
                            data[i+2] = '<efternamn>'+str(value[5])+'</efternamn>'
                    elif data[i+1] in dict_names['efternamn'][0]:
                        data[i] = '<fornamn_man>'+str(value[2])+'</fornamn_man>'
                        data[i+1] = '<efternamn>'+str(value[5])+'</efternamn>'
                    else:
                        data[i] = '<fornamn_man>'+str(value[2])+'</fornamn_man>'

    for i,j in enumerate(data):
        for key,value in dict_fornamn_kvn.items():
            if value[1] == j:
                if data[i-1] in dict_names['f??rnamn_kvinnor'][0]:
                    data[i-1] = '<fornamn_kvinnor>'+str(value[3])+'</fornamn_kvinnor>'
                    data[i] = '<fornamn_kvinnor>'+str(value[2])+'</fornamn_kvinnor>'
                    if data[i+1] in dict_names['efternamn'][0]:
                        data[i+1] = '<efternamn>'+str(value[5])+'</efternamn>'
                    if data[i+1] in dict_names['fornamn_kvinnor'][0]:
                        data[i+1] = '<fornamn_kvinnor>'+str(value[4])+'</fornamn_kvinnor>'
                        if data[i+2] in dict_names['efternamn'][0]:
                            data[i+2] = '<efternamn>'+str(value[5])+'</efternamn>'                
                elif data[i-1] not in dict_names['f??rnamn_kvinnor'][0]:
                    if data[i+1] in dict_names['f??rnamn_kvinnor'][0]:
                        data[i] = '<fornamn_kvinnor>'+str(value[2])+'</fornamn_kvinnor>'
                        data[i+1] = '<fornamn_kvinnor>'+str(value[4])+'</fornamn_kvinnor>'
                        if data[i+2] in dict_names['efternamn'][0]:
                            data[i+2] = '<efternamn>'+str(value[5])+'</efternamn>'
                    elif data[i+1] in dict_names['efternamn'][0]:
                        data[i] = '<fornamn_kvinnor>'+str(value[2])+'</fornamn_kvinnor>'
                        data[i+1] = '<efternamn>'+str(value[5])+'</efternamn>'
                    else:
                        data[i] = '<fornamn_kvinnor>'+str(value[2])+'</fornamn_kvinnor>'



    for i,j in enumerate(data):                   
        for key, value in dict_fornamn_man.items():
            if value[1] == j:
                data[i] = '<fornamn_man>'+str(value[2])+'</fornamn_man>'

    for i,j in enumerate(data):                   
        for key, value in dict_fornamn_kvn.items():
            if value[1] == j:
                data[i] = '<fornamn_kvinnor>'+str(value[2])+'</fornamn_kvinnor>'

    for i,j in enumerate(data):
        for key, value in dict_efternamn.items():
            if value[1] == j:
                data[i] = '<efternamn>'+str(value[2])+'</efternamn>'

    for i,j in enumerate(data):
        for key, value in dict_fornamn_man.items():
            value_s = value[1] + 's'
            if value_s == j:
                if value[2][-1] == 's': 
                    data[i] = '<fornamn_man>'+str(value[2])+'</fornamn_man>'
                else:
                    data[i] = '<fornamn_man>'+str(value[2]+'s')+'</fornamn_man>'

    for i,j in enumerate(data):
        for key, value in dict_fornamn_kvn.items():
            value_s = value[1] + 's'
            if value_s == j:
                if value[2][-1] == 's':
                    data[i] = '<fornamn_kvinnor>'+str(value[2])+'</fornamn_kvinnor>'
                else:
                    data[i] = '<fornamn_kvinnor>'+str(value[2]+'s')+'</fornamn_kvinnor>'
    data = ' '.join(data)            

    output_data = data.replace(' $$$$ . ', '\n\n')
    
    return output_data
    
if __name__ == '__main__':

    output_data = identify(data)
