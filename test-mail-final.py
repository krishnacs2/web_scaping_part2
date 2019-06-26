from io import StringIO
import smtplib
import time
import imaplib
import email
from datetime import datetime, timedelta
from dateutil.parser import parse
import arrow
import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import requests
import openpyxl
from pandas import DataFrame
from datetime import datetime
import os, errno
import sys
import json
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from docx import Document

ORG_EMAIL   = "@alindus.net"
FROM_EMAIL  = "jessica" + ORG_EMAIL
FROM_PWD    = "PL5<m2QS"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

try:
	mail = imaplib.IMAP4_SSL(SMTP_SERVER)
	mail.login(FROM_EMAIL,FROM_PWD)
	mail.select('inbox')
	date = (datetime.today() - timedelta(1)).strftime("%d-%b-%Y")
	type, data = mail.search(None, '(SENTSINCE {date})'.format(date=date))
	mail_ids = data[0]

	id_list = mail_ids.split()
	
	def sentence_finder(text,word):
		sentences=sent_tokenize(text)
		return [sent for sent in sentences if word in word_tokenize(sent)]


	for i in reversed(id_list):
		typ, data = mail.fetch(bytes(i), '(RFC822)' )
		
		for response_part in data:
			if isinstance(response_part, tuple):
				try:
					msg = email.message_from_string(response_part[1].decode('utf-8'))
					#print(msg)
					email_subject = msg['subject']
					sender1 = msg['from']
					#print(msg['body'])
				except:
					pass
					
				#print(delta.days)			
				if msg.is_multipart():
					for part in msg.walk():
						ctype = part.get_content_type()
						cdispo = str(part.get('Content-Disposition'))
						# skip any text/plain (txt) attachments
						if ctype == 'text/plain' and 'attachment' not in cdispo:
							body = part.get_payload(decode=True)  # decode
							#print(body)
							s = re.sub('[^ a-zA-Z0-9,@.:]', '', str(body))
							#print(s)
							replaced = re.sub('rnrn', '. ', s)
							replaced = re.sub('rn', '. ', replaced)
							#print(replaced[3:])
							mail_subject = msg['subject']
							mail_body = replaced
							mail_body = replaced.encode('utf-8')
							
							#role
							strng = []	 
							strng.append(sentence_finder(str(mail_body),'Role'))
							#strng.append(sentence_finder(s,'nice'))
							#print(strng)
							str1 = ''.join(str(e) for e in strng)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str1)
							role = str(str1)[1:-1]
							role = role.replace("'", "")
							stopwords = ['Role','Role:',':']
							querywords = role.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							role = ' '.join(resultwords)
							#print(role)
							
							#title
							strng = []	 
							strng.append(sentence_finder(str(mail_body),'Title'))
							#strng.append(sentence_finder(s,'nice'))
							#print(strng)
							str1 = ''.join(str(e) for e in strng)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str1)
							role = str(str1)[1:-1]
							role = role.replace("'", "")
							stopwords = ['Title','Title:',':']
							querywords = role.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							title = ' '.join(resultwords)
							#print(role)

							#duration
							strng_duration = []	 
							strng_duration.append(sentence_finder(str(mail_body),'Duration'))
							str_durtn = ''.join(str(e) for e in strng_duration)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str_durtn)
							duration = str(str_durtn)[1:-1]
							duration = duration.replace("'", "")
							stopwords = ['Duration','Duration:',':']
							querywords = duration.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							duration = ' '.join(resultwords)
							#print(duration)
							
							#Experience
							strng_exp= []	 
							strng_exp.append(sentence_finder(str(mail_body),'Exp'))
							str_exp = ''.join(str(e) for e in strng_exp)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str_exp)
							experience = str(str_exp)[1:-1]
							experience = experience.replace("'", "")
							stopwords = ['Exp','Exp:',':']
							querywords = experience.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							experience = ' '.join(resultwords)
							#print(experience)
							
							#client
							strng_client= []	 
							strng_client.append(sentence_finder(str(mail_body),'Client'))
							str_client = ''.join(str(e) for e in strng_client)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str_client)
							client1 = str(str_client)[1:-1]
							client1 = client1.replace("'", "")
							stopwords = ['Client','Client:',':']
							querywords = client1.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							client1 = ' '.join(resultwords)
							#print(client1)
							
							#Location
							strng_loc= []	 
							strng_loc.append(sentence_finder(str(mail_body),'Location'))
							str_loc = ''.join(str(e) for e in strng_loc)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str_loc)
							location_area = str(str_loc)[1:-1]
							location_area = location_area.replace("'", "")
							stopwords = ['Location','Location:',':']
							querywords = location_area.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							location_area = ' '.join(resultwords)
							#print(location_area)
							
							#Type
							strng_type= []	 
							strng_type.append(sentence_finder(str(mail_body),'Type'))
							str_type = ''.join(str(e) for e in strng_type)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str_type)
							job_type = str(str_type)[1:-1] 
							job_type = job_type.replace("'", "")
							stopwords = ['Type','Type:','type','type:',':']
							querywords = job_type.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							job_type = ' '.join(resultwords)
							#print(job_type)
							
							#Position type
							strng_p_type= []	 
							strng_p_type.append(sentence_finder(str(mail_body),'Position'))
							str_p_type = ''.join(str(e) for e in strng_p_type)
							#print( ", ".join( repr(e) for e in strng ) )
							#print(str_p_type)
							job_pos_type = str(str_p_type)[1:-1] 
							job_pos_type = job_pos_type.replace("'", "")
							stopwords = ['Position','Position:',':','Type','Type:','type','type:']
							querywords = job_pos_type.split()
							resultwords  = [word for word in querywords if word not in stopwords]
							job_pos_type = ' '.join(resultwords)
							#print(job_pos_type)
							
							try:
								text=nltk.word_tokenize(str(email_subject))
								tokens = nltk.pos_tag(text)
								#tags = pos_tag(text, tagset='universal')
								#print(tokens)
								#print(tags)
								all_words = []
								for tag in tokens:
									if tag[1] in {'NNP','IN'} and tag[0] not in {'Need'}:
										all_words.append(tag[0])		
										title_source = ' '.join(all_words)		
								#print(r.json())
								#print("Query is : " + r.json()['query'])
								#print("intent is : "+ r.json()['topScoringIntent']['intent'] +" - "+ str(r.json()['topScoringIntent']['score']))
								data = {}
								#data['query'] = r.json()['query']
								if role is None:
									if len(title) <= 30 :
										data['role'] = title
									else:
										data['role'] = ""
								else:
									if len(role) <= 30 :
										data['role'] = role
									else:
										data['role'] = ""

								if len(duration) <= 30 :
									data['duration'] = duration
								else:
									data['duration'] = ""

								if len(experience) <= 30 :
									data['exp'] = experience
								else:
									data['exp'] = ""

								if len(client1) <= 30 :
									data['client'] = client1
								else:
									data['client'] = ""

								#web.debug("HI")
								#web.debug(location_area)
								if len(location_area) <= 30 :
									data['location'] = location_area
								else:
									data['location'] = ""

								if job_type is None:
									if len(job_type) <= 30 :
										data['type'] = job_type
									else:
										data['type'] = ""
								else:
									if len(job_pos_type) <= 30 :
										data['type'] = job_pos_type
									else:
										data['type'] = ""	
								data['intent'] = title_source
								data['from'] = sender1	
								json_data = json.dumps(data)
								print(json_data)   

							except Exception as e:
								pass
								print(str(e))
								#pass
							
				# not multipart - i.e. plain text, no attachments, keeping fingers crossed
				else:
					body = msg.get_payload(decode=True)
					s = re.sub('[^ a-zA-Z0-9]', '', str(body))
					#print(s)
					replaced = re.sub('rnrn', '.', s)
					replaced = re.sub('rn', '. ', replaced)
					#print(replaced[3:])
					mail_body = replaced
					mail_body = replaced.encode('utf-8')
					
					#role
					strng = []	 
					strng.append(sentence_finder(str(mail_body),'Role'))
					#strng.append(sentence_finder(s,'nice'))
					#print(strng)
					str1 = ''.join(str(e) for e in strng)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str1)
					role = str(str1)[1:-1]
					role = role.replace("'", "")
					stopwords = ['Role','Role:',':']
					querywords = role.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					role = ' '.join(resultwords)
					#print(role)
					
					#title
					strng = []	 
					strng.append(sentence_finder(str(mail_body),'Title'))
					#strng.append(sentence_finder(s,'nice'))
					#print(strng)
					str1 = ''.join(str(e) for e in strng)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str1)
					role = str(str1)[1:-1]
					role = role.replace("'", "")
					stopwords = ['Title','Title:',':']
					querywords = role.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					title = ' '.join(resultwords)
					#print(role)

					#duration
					strng_duration = []	 
					strng_duration.append(sentence_finder(str(mail_body),'Duration'))
					str_durtn = ''.join(str(e) for e in strng_duration)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str_durtn)
					duration = str(str_durtn)[1:-1]
					duration = duration.replace("'", "")
					stopwords = ['Duration','Duration:',':']
					querywords = duration.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					duration = ' '.join(resultwords)
					#print(duration)
					
					#Experience
					strng_exp= []	 
					strng_exp.append(sentence_finder(str(mail_body),'Exp'))
					str_exp = ''.join(str(e) for e in strng_exp)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str_exp)
					experience = str(str_exp)[1:-1]
					experience = experience.replace("'", "")
					stopwords = ['Exp','Exp:',':']
					querywords = experience.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					experience = ' '.join(resultwords)
					#print(experience)
					
					#client
					strng_client= []	 
					strng_client.append(sentence_finder(str(mail_body),'Client'))
					str_client = ''.join(str(e) for e in strng_client)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str_client)
					client1 = str(str_client)[1:-1]
					client1 = client1.replace("'", "")
					stopwords = ['Client','Client:',':']
					querywords = client1.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					client1 = ' '.join(resultwords)
					#print(client1)
					
					#Location
					strng_loc= []	 
					strng_loc.append(sentence_finder(str(mail_body),'Location'))
					str_loc = ''.join(str(e) for e in strng_loc)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str_loc)
					location_area = str(str_loc)[1:-1]
					location_area = location_area.replace("'", "")
					stopwords = ['Location','Location:',':']
					querywords = location_area.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					location_area = ' '.join(resultwords)
					#print(location_area)
					
					#Type
					strng_type= []	 
					strng_type.append(sentence_finder(str(mail_body),'Type'))
					str_type = ''.join(str(e) for e in strng_type)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str_type)
					job_type = str(str_type)[1:-1] 
					job_type = job_type.replace("'", "")
					stopwords = ['Type','Type:','type','type:',':']
					querywords = job_type.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					job_type = ' '.join(resultwords)
					#print(job_type)
					
					#Position type
					strng_p_type= []	 
					strng_p_type.append(sentence_finder(str(mail_body),'Position'))
					str_p_type = ''.join(str(e) for e in strng_p_type)
					#print( ", ".join( repr(e) for e in strng ) )
					#print(str_p_type)
					job_pos_type = str(str_p_type)[1:-1] 
					job_pos_type = job_pos_type.replace("'", "")
					stopwords = ['Position','Position:',':','Type','Type:','type','type:']
					querywords = job_pos_type.split()
					resultwords  = [word for word in querywords if word not in stopwords]
					job_pos_type = ' '.join(resultwords)
					#print(job_pos_type)
					
										
					try:
						text=nltk.word_tokenize(str(email_subject))
						tokens = nltk.pos_tag(text)
						#tags = pos_tag(text, tagset='universal')
						#print(tokens)
						#print(tags)
						all_words = []
						for tag in tokens:
							if tag[1] in {'NNP','IN'} and tag[0] not in {'Need'}:
								all_words.append(tag[0])		
								title_source = ' '.join(all_words)
						#print("Query is : " + r.json()['query'])
						#print("intent is : "+ r.json()['topScoringIntent']['intent'] +" - "+ str(r.json()['topScoringIntent']['score']))
						data = {}	
						if role is None:
							if len(title) <= 30 :
								data['role'] = title
							else:
								data['role'] = ""
						else:
							if len(role) <= 30 :
								data['role'] = role
							else:
								data['role'] = ""

						if len(duration) <= 30 :
							data['duration'] = duration
						else:
							data['duration'] = ""

						if len(experience) <= 30 :
							data['exp'] = experience
						else:
							data['exp'] = ""

						if len(client1) <= 30 :
							data['client'] = client1
						else:
							data['client'] = ""

						#web.debug("HI")
						#web.debug(location_area)
						if len(location_area) <= 30 :
							data['location'] = location_area
						else:
							data['location'] = ""

						if job_type is None:
							if len(job_type) <= 30 :
								data['type'] = job_type
							else:
								data['type'] = ""
						else:
							if len(job_pos_type) <= 30 :
								data['type'] = job_pos_type
							else:
								data['type'] = ""
	
						data['intent'] = title_source
						data['from'] = sender1	
						json_data = json.dumps(data)

					except Exception as e:
						pass
						print(str(e))
						#pass
						
#print(body)
except Exception as e:
	pass
	print(str(e))
	