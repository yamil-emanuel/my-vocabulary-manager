from django.http import request
from django.shortcuts import redirect
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q #Allows using multiple conditionals into a query
from django.core import serializers
from django.urls import reverse

from MODULOS.SCRAPPER.models import *

from MODULOS.SCRAPPER.scrapper import *


def newEntry(request,lang,word):
	"""Recives lang and word parameters, with it creates an Definiciones instance in order 
	to gather necessary data. Once it's done the user will be redirected to APIRequest.
	"""


	lang_filter={'es':'spanish', 'en':'english', 'ger':'german'} #Filter
	user_input=Definiciones(word,lang) #Create a Definiciones instance 

	new_entry=Vocabulary(
			base_word=user_input.word,
			base_lang=user_input.lang,
			spanish=user_input.spanish,
			english=user_input.english,
			german=user_input.german,
			es_definition=user_input.es_definition,
			en_definition=user_input.en_definition,
			ger_definition=user_input.ger_definition)
	new_entry.save()

	return HttpResponseRedirect(reverse(APIRequest, kwargs={'lang':lang, 'word':word})) #Redirects to APIRequest
	

def APIRequest(request,lang,word):
	""" Verifies what kind of request is coming in, process it verifing if an object with 
	these attributes already exists in the database. If there aren't any match, the request
	will be redirected to newEntry in order to gather the necesary data.
	"""


	template="""
	<div id="entry">
		<h1 id="word">{}</h1>
		<h5 id="definition">{}</h5>
	</div>
	"""

	if lang=='es':
		if Vocabulary.objects.filter(spanish=word).exists():
			data=Vocabulary.objects.get(spanish=word)
			return HttpResponse(template.format(data.spanish.upper(), data.es_definition))
		else:
			return HttpResponseRedirect(reverse(newEntry, kwargs={'lang':lang,'word':word}))


	elif lang=="en":
		if Vocabulary.objects.filter(english=word).exists():
			data=Vocabulary.objects.get(english=word)
			return HttpResponse(template.format(data.english.upper(), data.en_definition))
		else:
			return HttpResponseRedirect(reverse(newEntry, kwargs={'lang':lang,'word':word}))


	elif lang=="ger":
		if Vocabulary.objects.filter(german=word).exists():
			data=Vocabulary.objects.get(german=word)
			return HttpResponse(template.format(data.german.upper(), data.ger_definition))
		else:
			return HttpResponseRedirect(reverse(newEntry, kwargs={'lang':lang,'word':word}))
	

	else:
		return HttpResponse("LANGUAGE NOT AVAIABLE")


def translate(request,baseLang,targetLang, word):
	"""Translate API. Recives baseLang (user's mothertonge), targetLang (target language) and the word.
	Process the request bringing the translation's data into a template. In case the word doesn't exist in the db
	the request will be redirected to newEntry 
	"""
	
	template="""
	<div id='entry'>
		<h1 class="word">{}</h1>
		<h5 class="definition">{}<h5>
		<h3 class="word">{}</h3>
		<h5 class="definition">{}</h5>
	</body>
	"""

	if baseLang == "es":
		if Vocabulary.objects.filter(spanish=word).exists():
			data=Vocabulary.objects.get(spanish=word)
			target={ 'en':[data.english,data.en_definition], 'ger':[data.german,data.ger_definition] }
			return HttpResponse(template.format(data.spanish.upper(), data.es_definition, target[targetLang][0].upper(), target[targetLang][1]))

		else:
			return HttpResponseRedirect(reverse(newEntry, kwargs={'lang':baseLang,'word':word}))


	elif baseLang == "en":
		if Vocabulary.objects.filter(english=word).exists():
			data=Vocabulary.objects.get(english=word)
			target={ 'es':[data.spanish,data.es_definition], 'ger':[data.german,data.ger_definition] }
			return HttpResponse(template.format(data.english.upper(), data.en_definition, target[targetLang][0].upper(), target[targetLang][1]))

		else:
			return HttpResponseRedirect(reverse(newEntry, kwargs={'lang':baseLang,'word':word}))


	elif baseLang == "ger":

		if Vocabulary.objects.filter(german=word).exists():
			data=Vocabulary.objects.get(german=word)
			target={ 'es':[data.spanish, data.es_definition], 'en':[data.english, data.en_definition] }
			return HttpResponse(template.format(data.german.upper(), data.ger_definition, target[targetLang][0].upper(), target[targetLang][1]))

		else:
			return HttpResponseRedirect(reverse(newEntry, kwargs={'lang':baseLang,'word':word}))


	else:
		return HttpResponse("LANGUAGE NOT AVAIABLE")


def errorLog(request):
	#Returns a Json of every dictionary object that contains any definition error.

	data=Vocabulary.objects.filter( Q(es_definition="NOT FOUND") | Q(en_definition="NOT FOUND") | Q(ger_definition="NOT FOUND") )
	f=serializers.serialize("json", data)

	return HttpResponse (f)