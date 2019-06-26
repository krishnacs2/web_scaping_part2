import urllib.request as urllib
from bs4 import BeautifulSoup
#from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
#import urllib
#import urllib.request
from requests.exceptions import ConnectionError
import json
import nltk
import re
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
#https://github.com/MarioVilas/googlesearch
 
def clean_me(html):
	soup = BeautifulSoup(html) # create a new bs4 object from the html data loaded
	for script in soup(["script"]): 
		script.extract()
	text = soup.get_text()
	return text

def Gsearch(self):
	count = 0
	try :
	 from googlesearch import search
	except ImportError:
	 print("No Module named 'google' Found")
	for url in search(query=self,lang='en',num=2,stop=2,pause=2):
		count += 1
		print (count)
		print(url + '\n')
		 
		html = urllib.urlopen(url).read()
		soup = BeautifulSoup(html)

		# kill all script and style elements
		for script in soup(["script", "style"]):
			script.extract()    # rip it out

		# get text
		text1 = soup.get_text()

		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text1.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("\n."))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)
		text = re.sub('[^a-zA-Z0-9\n\.]', ' ', text)
		url = "http://localhost:8000/getSentiment"
		print1=sent_tokenize(text1)
		tct = [re.sub('[^a-zA-Z0-9.]', ' ', _) for _ in print1]
		sss = []
		for text in tct:
			tokenized_sentence = nltk.word_tokenize(text)

			sid = SentimentIntensityAnalyzer()
			pos_word_list=[]
			neu_word_list=[]
			neg_word_list=[]

			for word in tokenized_sentence:
				if (sid.polarity_scores(word)['compound']) >= 0.1:
					pos_word_list.append(word)
				elif (sid.polarity_scores(word)['compound']) <= -0.1:
					neg_word_list.append(word)
				else:
					 neu_word_list.append(word)                

			print('Positive words list:',pos_word_list)        
			print('Neutral words list:',neu_word_list)    
			print('Negative words list:',neg_word_list) 
			score = sid.polarity_scores(text)
			#print('\nScores:', score)


			posit = sid.polarity_scores(text)['pos']
			negat = sid.polarity_scores(text)['neg']
			neut = sid.polarity_scores(text)['neu']
			
			if negat*100 > 50:
				sss.append(text)
				sss.append(negat*100)
			
			print('\n')

			print('Positive score is',sid.polarity_scores(text)['pos']*100,'%')
			print('Neutral score is',sid.polarity_scores(text)['neu']*100,'%')
			print('Negative score',sid.polarity_scores(text)['neg']*100,'%')

			if posit >= negat and posit >=neut :
				print('Overall Sentiment score: Positive')
			elif negat > posit and negat>=neut:
				print('Overall Sentiment score : Negative')
			else:
				print('Overall Sentiment score : Neutral')


		print(sss)		#txt= clean_me(html)
		#print1=sent_tokenize(text1)
		#tct = [re.sub('[^a-zA-Z0-9.]', ' ', _) for _ in print1]
		#print(tct)
		#print(len(tct))
		#print(payload)
	
		
if __name__=='__main__':
   #Gsearch_python("Revanth\"Reddy\"")
   Gsearch("Revanth\"Reddy\"")