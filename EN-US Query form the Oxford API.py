# These lines provide some basic info for the script to work. Import relevant libraries
import json
import time
import requests
# use your own keys that you can get by submitting to a "Prototype" account in the Oxford API
app_id = "APP ID"
app_key = "APP KEY"
# This determines from which part of the API the script will pull data
endpoint = "entries"
# Which corpus? American or British?
language_code = "en-us"







# Here you feed the list of words in quotes, and spearated by commas. It was the best I could think of.
thislist = ["LIST", "OF", "WORDS"]
# It starts a loop according ot the number of words the list.
for x in thislist:
	# Give it a 2 seconds break because the API's "Prototype" account has a limit of queries per minute.
	time.sleep(2)
	# This variable will store the word of the current loop.
	word_id = x
	# This variable will store the query url specific to the given word.
	url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
	# This variable stores the basic information we need to inform the server in order to get access to it.
	r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
	# If all went well (the word was found in the corpus), this variable will store a huge ugly file with the precious data we need.
	wordObject = json.loads(r.text)
	# Here another loop starts. We now try to get the precious stuff we need.
	try:
		# This variable will store the number of meanings for this single word.
		numberResults = len(wordObject["results"])
		# Then here it starts a loop acording to the number of meanings available.
		for nResults in range(numberResults):

			# This variable will store the number of lexical entries. One word may have 'verb', 'noun', 'adjective', 'adverb'.
			numberLexicalEntries = len(
				wordObject["results"][nResults]["lexicalEntries"])
			# Here we start another loop according to the number of meanings for each lexical entry. One 'verb' may have more than one meaning.
			for lexEn in range(numberLexicalEntries):
				# This variable will store the number of entries for this meaning.
				numberEntries = len(wordObject["results"][nResults]
									["lexicalEntries"][lexEn]["entries"][0]["senses"])
				# This variable will store the number of senses for each meaning.
				for nSenses in range(numberEntries):

					# Then we try to get it
					try:  # first definition & first example
						# print first def and ex
						print("\n",wordObject["word"], " @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["lexicalCategory"]["text"], " @ ",lexEn+1,"_",nSenses+1," ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["senses"][nSenses]["definitions"][0],
							" @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["senses"][nSenses]["examples"][0], " @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["pronunciations"][1]["phoneticSpelling"])
					# If there is no usage example available, we'll print 'missing example' in that field.
					except:
						print("\n",wordObject["word"], " @ ",wordObject["results"][nResults]["lexicalEntries"][lexEn]["lexicalCategory"]["text"], " @ ",lexEn+1,"_",nSenses+1," ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"]
						[0]["senses"][nSenses]["definitions"][0], " @ ", "missing example"," @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["pronunciations"][1]["phoneticSpelling"])

					# Here we try for a sub definition of the main meaning.
					try:  # try for sub definition
						try:
							numberSubSenses = len(wordObject["results"][nResults]["lexicalEntries"]
											[lexEn]["entries"][0]["senses"][nSenses]["subsenses"])
							for nSubSenses in range(numberSubSenses):
								print("\n",wordObject["word"], " @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["lexicalCategory"]["text"], " @ ",lexEn+1,"_",nSenses+1,"_",nSubSenses+1, wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["senses"][nSenses]["subsenses"][nSubSenses]["definitions"][0],
										" @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["senses"][nSenses]["subsenses"][nSubSenses]["examples"][0], " @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["pronunciations"][1]["phoneticSpelling"])
						except:
							pass


								

					# If there's no example for the sub meaning, we'll print 'missing sub example' for that field.
					except:
						print("\n",wordObject["word"], " @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["lexicalCategory"]["text"], " @ ",lexEn+1,"_",nSenses+1, wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["senses"]
									[nSenses]["subsenses"][nSubSenses]["definitions"][0], " @ ", "missing sub example", " @ ", wordObject["results"][nResults]["lexicalEntries"][lexEn]["entries"][0]["pronunciations"][1]["phoneticSpelling"])

	except:
		# If there is nothing more we can pull from the given word, the script here proceeds to the next one on the list.
		pass
