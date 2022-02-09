import requests
from bs4 import BeautifulSoup


class Urls:
	def __init__(self):
		self.definition_es ='https://www.wordreference.com/definicion/{}'
		self.definition_en ='https://www.wordreference.com/definition/{}'
		self.definition_ger ='https://www.duden.de/rechtschreibung/{}'

		#ENGLISH <-> SPANISH
		self.en_es_translation='https://www.wordreference.com/es/translation.asp?tranword={}'
		self.es_en_translation='https://www.wordreference.com/es/en/translation.asp?spen={}'

		#GERMAN <-> ENGLISH
		self.en_ger_translation='https://www.wordreference.com/ende/{}'
		self.ger_en_translation='https://www.wordreference.com/deen/{}'

		#GERMAN <-> SPANISH
		self.es_ger_translation="https://www.wordreference.com/esde/{}"
		self.ger_es_translation="https://www.wordreference.com/dees/{}"

class Palabra:

	def __init__(self, word,lang):
		self.word = word
		self.lang=lang

class Traducciones(Palabra):
	def wordCleaner(self,word):
		#Removes extra characters from words
		#Explample 'sofa, ' ---> 'sofa'
		return word.replace(",","").replace(" ","").replace(".","").replace("/","")

	def toSpanish(self,lang):
		#Traduce del idioma base al español

		if self.lang!="es":
			urls_list = {'en' : urls.en_es_translation, 'ger' : urls.ger_es_translation }

			translation_data = requests.get((urls_list[self.lang]).format(self.word))
			soup_definition = BeautifulSoup(translation_data.content, 'lxml')
		
			#Buscar objetos translate
			definition_raw=(soup_definition.find_all(attrs={'class':'ToWrd'}))[1]
			return self.wordCleaner(definition_raw.get_text().split(" ")[0])
		else:
			return self.wordCleaner(self.word)
	
	def toEnglish(self,lang):
		#traduce del idioma base al inglés
		if self.lang != "en":
			urls_list = {'es' : urls.es_en_translation, 'ger' : urls.ger_en_translation }

			translation_data = requests.get((urls_list[self.lang]).format(self.word))
			soup_definition = BeautifulSoup(translation_data.content, 'lxml')
		
			#Buscar objetos translate
			try:
				definition_raw=(soup_definition.find_all(attrs={'class':'ToWrd'}))[1]
				return self.wordCleaner(definition_raw.get_text().split(" ")[0])
			except IndexError:
				return "NOT FOUND"
				
		else:
			return self.wordCleaner(self.word)

	def toGerman(self,lang):
		#Traduce del idioma base al alemán

		if self.lang != "ger":
			urls_list = {'es' : urls.es_ger_translation, 'en' : urls.en_ger_translation }

			translation_data = requests.get((urls_list[self.lang]).format(self.word))
			soup_definition = BeautifulSoup(translation_data.content, 'lxml')
		
			#Buscar objetos translate
			try:
				definition_raw=(soup_definition.find_all(attrs={'class':'ToWrd'}))[1]
				return self.wordCleaner(definition_raw.get_text().split(" ")[0])
			except IndexError:
				definition_raw=(soup_definition.find_all(attrs={'class':'ToWrd'}))[0]
				return self.wordCleaner(definition_raw.get_text().split(" ")[0])
		else:
			return self.wordCleaner(self.word)

	def __init__(self,word,lang, english=None, german=None, spanish=None):
		super().__init__(word, lang)

		self.spanish=self.toSpanish(self)
		self.english=self.toEnglish(self)
		self.german=self.toGerman(self)

class Definiciones(Traducciones):
		#Dictionary with definition's urls
	def getDefinition(self,word,lang):

		urls_list={
		'es': [urls.definition_es , self.spanish],
		'en': [urls.definition_en , self.english],
		'ger': [urls.definition_ger , self.german]
		}

		if lang != 'ger':
			#making request
			url_definition=requests.get( (urls_list[lang][0] ).format( urls_list[lang][1]) )
			soup_definition = BeautifulSoup(url_definition.content, 'lxml')
			#Spanish/English definition
			definition=(soup_definition.find_all(attrs={'class':'entry'}))

			try:
				#In case there's another definition, return them. 
				definitions_raw = (soup_definition.find_all(attrs={'class':'trans clickable'}))
				definitions= [defi.get_text() for defi in definitions_raw ]
				definitions.append(definition.get_text())
				#Return multiple definitions
				return definitions
			except:
				try:
					#If there aren't other definitions, returns only one
					return definition[0].get_text()
				except IndexError:
					#If there aren't any definitions, returns NOT FOUND
					return "NOT FOUND"

		else:
			ger_umlaud_correction=urls_list[lang][1].replace("ü","ue").replace("ä","ae").replace("ö","oe")
			url_definition=requests.get((urls_list[lang][0]).format(ger_umlaud_correction))
			soup_definition_german = BeautifulSoup(url_definition.content, 'lxml')
			#Get relevant data for the R's functions (RegularCheck and ReflexiveCheck).
			

			try:
				raw_data=list(soup_definition_german.find_all(attrs={'class':'enumeration__text'}))
				return raw_data[0].get_text()

			except IndexError:
				try:
					raw_data=list(soup_definition_german.find_all(attrs={'id':'bedeutung'}))
					return raw_data[0].get_text().replace("\n","").replace("Bedeutung","").replace("ⓘ","")
				except IndexError:
					try:
						raw_data=list(soup_definition_german.find_all(attrs={'class':'tran'}))
						return raw_data[0].get_text().replace("\n","").replace("Bedeutung","").replace("ⓘ","")
					except:
						return "NOT FOUND"




	def __init__(self,word, lang, spanish=None, english=None, german=None, es_definition=None, ger_definition=None, en_definition=None):
		super().__init__(word,lang,spanish, english, german)
		self.es_definition=self.getDefinition(self.spanish,"es")
		self.en_definition=self.getDefinition(self.english,"en")
		self.ger_definition=self.getDefinition(self.german, "ger")

#Inicializar clase con las urls necesarias
urls=Urls()
#Crear instancia de clase
#	x=Definiciones("sofa","es")
