# LT2311_English_Pseudo
Pseudonymization of L2 English

Original repo: https://github.com/SamirYousuf/Pseudonymization 

Adapting the original code, for Swedish pseudonymization, to work for English.



### Professions:
Trying to replace profession names in English.
The file in Swedish has the following format:

,SSYK 2012 kod,Yrkesbenämning
0,2173,3D-designer
1,2173,3D-grafiker

- First column --> line count
- Second column --> SSYK 2012 code, which stands for "Standard för svensk yrkesklassificering". SSYK is based on the International Standard Classification of Occupation (ISCO), which is one of the main international classifications for jobs. SSYK is adapted to today's Swedish professional structure.

https://www.scb.se/dokumentation/klassifikationer-och-standarder/standard-for-svensk-yrkesklassificering-ssyk/
https://www.ilo.org/public/english/bureau/stat/isco/

- Third column --> job name

Two options were considered:
- Translating the jobs into English (not the most reliable option)
- Finding a job dataset in English and kept the same format as the original file in Swedish. However, the SSYK codes won't be included. As an alternative, ISCO codes were thought to replace the SSYK codes, but it was not possible to find a dataset that already includes them and following the occupational classifications proposed in ISCO-08 was descarded as an option.





-----------------------------------

#### There are three jupyter notebooks used for modifying the following csv files:
##### list_matching_simple.py
- cityCountry.csv
- _cityCountry.csv

##### list_matching_medium.py
- city_country.csv

##### list_matching_complex.py 
- city_country_population.csv
- _city_country_population.csv

The steps and logic followed for modifying each document are the same (AS DESCRIBED BELOW), with a few small differences. The functions 'cleaning_trans', 'swe_eng_dict' and 'rewriting_file' are common to all documents, however, functions 'extracting_countries' and 'final_data' are adapted to the inner structure of each file. While 'cityCountry.csv' and '_cityCountry.csv' have two columns ('Cities', 'Countries'), 'city_country.csv' consists of three columns (line count, 'Cities', Countries'), and finally 'city_country_population.csv' and '_city_country_population.csv' are made up of four columns (line count, 'Cities', 'Countries', 'Population'). Even though this whole process could have been performed in a single document, in the interest of clarity, it was decided to split into different notebooks. 



Jupyter Notebook --> list_matching_complex.py

#### def extracting_countries:
- Abrimos y leemos el archivo csv.
- Obtenemos header.
- Iteramos por las filas del archivo (ya que estamos leyendo el csv como si fuera una tabla dispuesta de filas y columnas).
- El tercer elemento de cada fila corresponde al nombre de país.
- Ya que los países se repiten en diferentes filas, creamos una lista donde cada país es introducido si no lo está ya. De esta manera, ningún país se repetirá en la lista.


#### translation:
- Take the list of all countries in Swedish, that is, the output from 'extracting_countries' and translate it (manually) to English with Google Translate. I originally thought of using a translation API to automate the process but it did not work because of time constraints (iba a tardar más en hacerlo funcionar que en lo que se tarda en hacerlo manualmente para 4 archivos). However, it could be improved in the future.


#### def cleaning_trans:
- Since the translation list contains some whitespaces at both the initial and last position in some
of the country names due to Google Translate somehow modifying the format, this function will clean the data and turn it into the appropriate format.


#### def swe_eng_dict:
- This function takes two arguments, that is, the list of all countries in Swedish from the file 'city_country.csv' and the list  of countries translated to English.

- We use zip() and dict() to make a dictionary out of the two aforementioned lists, since the elements from both lists follow the same order. The dictionaty has the Swedish country names as keys and the English translation as the values. This way, when we call for the key, we will get the value.

- Given that some country names remain the same in the two languages, this function checks if the same name is included in both lists. If so, as is the case of 'Argentina', it only means the country is called the same in Swedish and English. On the other hand, 'Italy' will not be present in our two lists since the name is spelled differently. The output of the function will be therefore a list with only those country names that were not spelled the same.


#### final_data:
- Open and read the original file (city_country.csv).
- We make a new empty list where we will add the first line of 'city_country.csv' as the header of our table. Next, we check if the country name in each line is in our dictionary. If it is not, the original line is added to the new list. If, on the contrary, the country name is a key in the dictionary, we add the line count, the city name and the translated country name (i.e., the key's value - {key = Swedish country name: value = English country name}). Commas and new lines are added to the elements of the new list with the intention of formatting.


#### rewriting_file:
- This function takes as arguments the original file that we need to modify and rewrites it with the new information contained in the second argument, which is the output from 'final_data'. 






## Since neither Sweden not any city 

I realized that neither 'Sweden' nor any Swedish city were included in the csv files concerning city/country names. For that reason, I decided to use the list of cities in Sweden from 'cities_sweden.csv' to extend those city/country name lists with such information making them more exhaustive.

Files a los que vamos a meter Sweden y la lista de ciudades suecas:
- cityCountry.csv:
En el jupyter notebook 'list_maching_simple.py'


- _cityCountry.csv

- city_country.csv




## Fíjate y comenta si vas a probar con input.txt en el terminal:
- Si pones dos veces el mismo país, en teoría debería identificarlo como país_1 y cada vez que salga en el input text, debería reemplazarlo por el mismo país. 
Es decir:
Si yo digo: "I was born in Spain. I am currently living in Sweden but I also miss Spain."
Spain --> country_1 --> Replacement: Germany
Sweden --> country_2 --> Replacement: Andorra

"I was born in Germany. I am currently living in Andorra but I also miss Germany."
















