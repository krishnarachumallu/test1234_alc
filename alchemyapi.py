#!/usr/bin/env python
import urllib2
import json

ENDPOINTS = {}
BASE_URL = 'http://access.alchemyapi.com/calls'
API_KEY = ''



def init():
	"""	
	Initializes the SDK so it can send requests to AlchemyAPI for analysis.
	It loads the API key from api_key.txt and configures the endpoints.
	This function will be called automatically from the endpoint wrappers when needed.
	"""

	import sys
	try:
		# Open the key file and read the key
		f = open("api_key.txt", "r")
		key = f.read().strip()
	 	
		if key == '':
			#The key file should't be blank
			print 'The api_key.txt file appears to be blank, please copy/paste your API key in the file: api_key.txt'
			print 'If you do not have an API Key from AlchemyAPI, please register for one at: http://www.alchemyapi.com/api/register.html'
			sys.exit(0)
		elif len(key) != 40:
			#Keys should be exactly 40 characters long
			print 'It appears that the key in api_key.txt is invalid. Please make sure the file only includes the API key, and it is the correct one.'
			sys.exit(0)
		else:
			#setup the key
			global API_KEY
			API_KEY = key
			
			#Setup the endpoints
			global ENDPOINTS
			ENDPOINTS['sentiment'] = {}
			ENDPOINTS['sentiment']['url'] = '/url/URLGetTextSentiment'
			ENDPOINTS['sentiment']['text'] = '/text/TextGetTextSentiment'
			ENDPOINTS['sentiment']['html'] = '/html/HTMLGetTextSentiment'
			ENDPOINTS['sentiment_targeted'] = {}
			ENDPOINTS['sentiment_targeted']['url'] = '/url/URLGetTargetedSentiment'
			ENDPOINTS['sentiment_targeted']['text'] = '/text/TextGetTargetedSentiment'
			ENDPOINTS['sentiment_targeted']['html'] = '/html/HTMLGetTargetedSentiment'
			ENDPOINTS['author'] = {}
			ENDPOINTS['author']['url'] = '/url/URLGetAuthor'
			ENDPOINTS['author']['html'] = '/html/HTMLGetAuthor'
			ENDPOINTS['keywords'] = {}
			ENDPOINTS['keywords']['url'] = '/url/URLGetRankedKeywords'
			ENDPOINTS['keywords']['text'] = '/text/TextGetRankedKeywords'
			ENDPOINTS['keywords']['html'] = '/html/HTMLGetRankedKeywords'
			ENDPOINTS['concepts'] = {}
			ENDPOINTS['concepts']['url'] = '/url/URLGetRankedConcepts'
			ENDPOINTS['concepts']['text'] = '/text/TextGetRankedConcepts'
			ENDPOINTS['concepts']['html'] = '/html/HTMLGetRankedConcepts'
			ENDPOINTS['entities'] = {}
			ENDPOINTS['entities']['url'] = '/url/URLGetRankedNamedEntities'
			ENDPOINTS['entities']['text'] = '/text/TextGetRankedNamedEntities'
			ENDPOINTS['entities']['html'] = '/html/HTMLGetRankedNamedEntities'
			ENDPOINTS['category'] = {}
			ENDPOINTS['category']['url']  = '/url/URLGetCategory'
			ENDPOINTS['category']['text'] = '/text/TextGetCategory'
			ENDPOINTS['category']['html'] = '/html/HTMLGetCategory'
			ENDPOINTS['relations'] = {}
			ENDPOINTS['relations']['url']  = '/url/URLGetRelations'
			ENDPOINTS['relations']['text'] = '/text/TextGetRelations'
			ENDPOINTS['relations']['html'] = '/html/HTMLGetRelations'
			ENDPOINTS['language'] = {}
			ENDPOINTS['language']['url']  = '/url/URLGetLanguage'
			ENDPOINTS['language']['text'] = '/text/TextGetLanguage'
			ENDPOINTS['language']['html'] = '/html/HTMLGetLanguage'
			ENDPOINTS['text_clean'] = {}
			ENDPOINTS['text_clean']['url']  = '/url/URLGetText'
			ENDPOINTS['text_clean']['html'] = '/html/HTMLGetText'
			ENDPOINTS['text_raw'] = {}
			ENDPOINTS['text_raw']['url']  = '/url/URLGetRawText'
			ENDPOINTS['text_raw']['html'] = '/html/HTMLGetRawText'
			ENDPOINTS['text_title'] = {}
			ENDPOINTS['text_title']['url']  = '/url/URLGetTitle'
			ENDPOINTS['text_title']['html'] = '/html/HTMLGetTitle'
			ENDPOINTS['feeds'] = {}
			ENDPOINTS['feeds']['url']  = '/url/URLGetFeedLinks'
			ENDPOINTS['feeds']['html'] = '/html/HTMLGetFeedLinks'
			ENDPOINTS['microformats'] = {}
			ENDPOINTS['microformats']['url']  = '/url/URLGetMicroformatData'
			ENDPOINTS['microformats']['html'] = '/html/HTMLGetMicroformatData'

		# Close file
		f.close()
	except IOError:
		#The file doesn't exist, so show the message and create the file.
		print 'API Key not found! Please copy/paste your API key into the file: api_key.txt'
		print 'If you do not have an API Key from AlchemyAPI, please register for one at: http://www.alchemyapi.com/api/register.html'
		
		#create a blank key file
		open('api_key.txt', 'a').close()
		sys.exit(0)
	except Exception as e:
		print e



def setkey(key):
	"""
	Writes the API key to api_key.txt file. It will create the file if it doesn't exist.
	This function is intended to be called from the Python command line using: python -c 'import alchemyapi;alchemyapi.setkey("API_KEY");'
	If you don't have an API key yet, register for one at: http://www.alchemyapi.com/api/register.html
	
	INPUT:
	key -> Your API key from AlchemyAPI. Should be 40 hex characters
	
	OUTPUT:
	none
	"""

	#write the key to the file
	f = open('api_key.txt','w')
	f.write(key)
	f.close()



def sentiment(flavor, data, options={}):
	"""
	Calculates the sentiment for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/sentiment-analysis/
	For the docs, please refer to: http://www.alchemyapi.com/api/sentiment-analysis/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	showSourceText -> 0: disabled (default), 1: enabled

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""

	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['sentiment']:
		return { u'status':'ERROR', u'statusInfo':u'sentiment analysis for ' + flavor + ' not available' }
		
	url = (BASE_URL +
			ENDPOINTS['sentiment'][flavor] + 
			'?apikey=' + API_KEY + 
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
		
	return analyze(url)



def sentiment_targeted(flavor, data, target, options={}):
	"""
	Calculates the targeted sentiment for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/sentiment-analysis/
	For the docs, please refer to: http://www.alchemyapi.com/api/sentiment-analysis/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	target -> the word or phrase to run sentiment analysis on.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	showSourceText	-> 0: disabled, 1: enabled

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""

	if API_KEY == '':
		init()
	
	if target is None or target == '':
		return { u'status':'ERROR', u'statusInfo':u'targeted sentiment requires a non-null target' }

	if flavor not in ENDPOINTS['sentiment_targeted']:
		return { u'status':'ERROR', u'statusInfo':u'targeted sentiment analysis for ' + flavor + ' not available' }
		
	url = (BASE_URL +
			ENDPOINTS['sentiment_targeted'][flavor] + 
			'?apikey=' + API_KEY + 
			'&target=' + target +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])

	return analyze(url)



def author(flavor, data, options={}):
	"""
	Extracts the author from a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/author-extraction/
	For the docs, please refer to: http://www.alchemyapi.com/api/author-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

	Availble Options:
	none

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()
	
	if flavor not in ENDPOINTS['author']:
		return { u'status':'ERROR', u'statusInfo':u'author extraction for ' + flavor + ' not available' }

	url = (BASE_URL +
			ENDPOINTS['author'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')


	for key in options:
		url += '&' + key + '=' + str(options[key])

	return analyze(url)


def keywords(flavor, data, options={}):
	"""
	Extracts the keywords from text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/keyword-extraction/
	For the docs, please refer to: http://www.alchemyapi.com/api/keyword-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
			
	Available Options:
	keywordExtractMode -> normal (default), strict
	sentiment -> analyze sentiment for each keyword. 0: disabled (default), 1: enabled. Requires 1 additional API transaction if enabled.
	showSourceText -> 0: disabled (default), 1: enabled.
	maxRetrieve -> the max number of keywords returned (default: 50)

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['keywords']:
		return { u'status':'ERROR', u'statusInfo':u'keyword extraction for ' + flavor + ' not available' }

	url = (BASE_URL + 
			ENDPOINTS['keywords'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)

        
def concepts(flavor, data, options={}):
	"""
	Tags the concepts for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/concept-tagging/
	For the docs, please refer to: http://www.alchemyapi.com/api/concept-tagging/ 
	
	Available Options:
	maxRetrieve -> the maximum number of concepts to retrieve (default: 8)
	linkedData -> include linked data, 0: disabled, 1: enabled (default)
	showSourceText -> 0:disabled (default), 1: enabled

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""

	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['concepts']:
		return { u'status':'ERROR', u'statusInfo':u'concept tagging for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['concepts'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)
        

def entities(flavor, data, options={}):
	"""
	Extracts the entities for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/entity-extraction/ 
	For the docs, please refer to: http://www.alchemyapi.com/api/entity-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
	linkedData -> include linked data on disambiguated entities. 0: disabled, 1: enabled (default) 
	coreference -> resolve coreferences (i.e. the pronouns that correspond to named entities). 0: disabled, 1: enabled (default)
	quotations -> extract quotations by entities. 0: disabled (default), 1: enabled.
	sentiment -> analyze sentiment for each entity. 0: disabled (default), 1: enabled. Requires 1 additional API transction if enabled.
	showSourceText -> 0: disabled (default), 1: enabled 
	maxRetrieve -> the maximum number of entities to retrieve (default: 50)

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['entities']:
		return { u'status':'ERROR', u'statusInfo':u'entity extraction for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['entities'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) + 
			'&outputMode=json') 
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)


def category(flavor, data, options={}):
	"""
	Categorizes the text for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/text-categorization/
	For the docs, please refer to: http://www.alchemyapi.com/api/text-categorization/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	showSourceText -> 0: disabled (default), 1: enabled

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['category']:
		return { u'status':'ERROR', u'statusInfo':u'text categorization for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['category'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json') 

	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)


def relations(flavor, data, options={}):
	"""
	Extracts the relations for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/relation-extraction/ 
	For the docs, please refer to: http://www.alchemyapi.com/api/relation-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	sentiment -> 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
	keywords -> extract keywords from the subject and object. 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
	entities -> extract entities from the subject and object. 0: disabled (default), 1: enabled. Requires one additional API transaction if enabled.
	requireEntities -> only extract relations that have entities. 0: disabled (default), 1: enabled.
	sentimentExcludeEntities -> exclude full entity name in sentiment analysis. 0: disabled, 1: enabled (default)
	disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
	linkedData -> include linked data with disambiguated entities. 0: disabled, 1: enabled (default).
	coreference -> resolve entity coreferences. 0: disabled, 1: enabled (default)  
	showSourceText -> 0: disabled (default), 1: enabled.
	maxRetrieve -> the maximum number of relations to extract (default: 50, max: 100)

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['relations']:
		return { u'status':'ERROR', u'statusInfo':u'relation extraction for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['relations'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')

	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)


def language(flavor, data, options={}):
	"""
	Detects the language for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/api/language-detection/ 
	For the docs, please refer to: http://www.alchemyapi.com/products/features/language-detection/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

	Available Options:
	none

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['language']:
		return { u'status':'ERROR', u'statusInfo':u'language detection for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['language'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')

	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)


def text_clean(flavor, data, options={}):
	"""
	Extracts the cleaned text (removes ads, navigation, etc.) for text, a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/
	For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	useMetadata -> utilize meta description data, 0: disabled, 1: enabled (default)
	extractLinks -> include links, 0: disabled (default), 1: enabled.

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['text_clean']:
		return { u'status':'ERROR', u'statusInfo':u'clean text extraction for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['text_clean'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json') 

	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)


def text_raw(flavor, data, options={}):
	"""
	Extracts the raw text (includes ads, navigation, etc.) for a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/ 
	For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	none

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['text_raw']:
		return { u'status':'ERROR', u'statusInfo':u'raw text extraction for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['text_raw'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)



def text_title(flavor, data, options={}):
	"""
	Extracts the title for a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/text-extraction/ 
	For the docs, please refer to: http://www.alchemyapi.com/api/text-extraction/
	
	INPUT:
	flavor -> which version of the call, i.e. text, url or html.
	data -> the data to analyze, either the text, the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	useMetadata -> utilize title info embedded in meta data, 0: disabled, 1: enabled (default) 

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['text_title']:
		return { u'status':'ERROR', u'statusInfo':u'title extraction for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['text_title'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)



def microformats(flavor, data, options={}):
	"""
	Parses the microformats for a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/microformats-parsing/
	For the docs, please refer to: http://www.alchemyapi.com/api/microformats-parsing/
	
	INPUT:
	flavor -> which version of the call, i.e.  url or html.
	data -> the data to analyze, either the the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
	
	Available Options:
	none

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['microformats']:
		return { u'status':'ERROR', u'statusInfo':u'microformat extraction for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['microformats'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')

	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)



def feeds(flavor, data, options={}):
	"""
	Detects the RSS/ATOM feeds for a URL or HTML.
	For an overview, please refer to: http://www.alchemyapi.com/products/features/feed-detection/ 
	For the docs, please refer to: http://www.alchemyapi.com/api/feed-detection/
	
	INPUT:
	flavor -> which version of the call, i.e.  url or html.
	data -> the data to analyze, either the the url or html code.
	options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

	Available Options:
	none

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""
	
	if API_KEY == '':
		init()

	if flavor not in ENDPOINTS['feeds']:
		return { u'status':'ERROR', u'statusInfo':u'feed detection for ' + flavor + ' not available' }
	
	url = (BASE_URL +
			ENDPOINTS['feeds'][flavor] +
			'?apikey=' + API_KEY +
			'&' + flavor + '=' + urllib2.quote(data) +
			'&outputMode=json')
	
	for key in options:
		url += '&' + key + '=' + str(options[key])
	
	return analyze(url)



def analyze(url):
	"""
	HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
	It makes the call, then converts the returned JSON string into a Python object. 
	
	INPUT:
	url -> the full URI encoded url

	OUTPUT:
	The response, already converted from JSON to a Python object. 
	"""

	try:
		#build the request with uri encoding
		req = urllib2.Request(url)
		f = urllib2.urlopen(req)
		return json.load(f)
	except Exception as e:
		print "error for url: ", url
		print e
		return { u'status':'ERROR', u'statusInfo':u'network-error' }

