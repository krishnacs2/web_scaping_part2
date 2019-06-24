# Importing the required packages
from googlesearch import search
import re
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import urllib
import urllib.request
from requests.exceptions import ConnectionError
import json
import xlwt
workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('My Worksheet',cell_overwrite_ok=True)


# Prompting the user to enter the words they want to search for
#query_1 = str(input("Enter the primary keyword:"))
#query_2 = str(input("Enter the secondary keyword:"))

#tld =["edu","gov","ca","in"]


#Concatenating the queries
#query = query_2+'"'+query_1+'"'

#Printing the query
#print("Your query is:",query)


with open('input.json') as inputu:
	data0= json.load(inputu)
	query = data0["query"]
	
print(query)

#Filtering the results based on time
#print("How old the results should be..?")
# “qdr:h” => last hour, “qdr:d” => last 24 hours, “qdr:m” => last month
#options = ["Any results","last hour", "last 24 hours", "last week","last month"]

'''
# Print out your options
for i in range(len(options)):
    print(str(i) + ":", options[i])
'''


# Take user input and get the corresponding item from the list
#inp = int(input("Enter a number: "))

with open('input.json') as fi:
	data01 = json.load(fi)
	inp = data01["inp"]

'''
inp = int(inp)
#print(inp)

if inp ==1:
	tbsuu = "qdr:h"
elif inp ==2:
	tbsuu = "qdr:d"
elif inp ==3:
	tbsuu = "qdr:w"
elif inp ==4:
	tbsuu = "qdr:m"
elif inp == 0:
	tbsuu = None
else:
	print("Invalid input")

#tbsu='"'+tbsuu+'"'
'''

#Storing the results in list of lists
url_list =[]
try:
    for url in search(query, stop=100,tbs ="qdr:w"):
	    url_list.append(url)
except urllib.error.HTTPError:
    print('503 error..! Try again after a while')	

#Json file with list of words we want to omit
with open("omitted_words.json") as f:
	data = json.load(f)
	omitted_words=data["omitted"]

print("############")	
print(url_list)
print(len(url_list))
print("##################")
	
	
'''
#Removing other than words
output = []
for x in url_list:
    if re.search('(/.)', x):
        sliptlist = re.findall(r"[\w']+", x)
        #sliptlist = re.split('; |,/.-',x)
        output.append(sliptlist)
		
#print(output)
'''

#Removing the omitted words from the urls obtained
def deleting(list_1,del_name):
    for sub_list in list_1:
        if del_name in sub_list:
            list_1.remove(sub_list)
    return list_1
	

for i in omitted_words:
	omitted_output = deleting(url_list,i)
	

filtered_url = omitted_output


with open("omitted_countries.json") as f1:
	data1 = json.load(f1)
	omitted_countries=data1["omitted_countries"]



# Removing duplicate words
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
	
print("++++++++")	
print("jj")
print("++++++++++")
#Removing the urls which are not required

#Removing the omitted words from the urls obtained
def deleting(list_1,del_name):
    for sub_list in list_1:
        if del_name in sub_list:
            list_1.remove(sub_list)
    return list_1
	

row = 0
column = 0
column1 = 1
column2 = 2 

print("********")	
print(filtered_url)
print(len(filtered_url))
print("**********")


for f in filtered_url:
	req = Request(f)
	try:
		r = urlopen(req,timeout=100)
		headers ={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
		r = requests.get(f,headers=headers)
		soup = BeautifulSoup(r.text,'html.parser')
		print(f)
		print("11111111111")
		print(soup)
		print("11111111111")
		worksheet.write(row, 0,f)
		workbook.save('Excel_Workbook.xls')
		row+=1
		#worksheet.write(row,column,f)
		#row+=1
		#writer = csv.writer(csv_out)
		#writer.writerows(f)       
		if r.status_code == 200 and len(r.text)==0:
			continue
			sliptlist = re.findall(r"[\w']+",soup.html.text)
			print("222222")
			print(sliptlist)
			print("222222")
			without_dup =Remove(sliptlist)
			#Removing single characters 
			without_single_char=[i for i in without_dup if len(i) > 1]
			#Removing items containing numbers
			without_num = [x for x in without_single_char if not any(x1.isdigit() for x1 in x)]
			#Joining the elements of the list using space
			res = " ".join(without_num)	
			for i in omitted_countries:
				omitted_countries_output = deleting(filtered_url,i)
		
	except HTTPError as e:
		print('The server couldn\'t fulfill the request.')
		print('Error code: ', e.code)
		#worksheet.write(row, column1,e.code) 
		#row+=1
		#writer = csv.writer(csv_out)
		#writer.writerows(e.code)
		worksheet.write(row,1,e.code)
		workbook.save('Excel_Workbook.xls')
		row+=1
		if e.code == 404  or e.code == 403 or e.code == 500:
			filtered_url.remove(f)
	except URLError as e:
		print('We failed to reach a server.')
		print('Reason: ', e.reason)
		#worksheet.write(row,column2,e.reason)
		#row+=1
		#writer = csv.writer(csv_out)
		#writer.writerows(f)
		worksheet.write(row,2,f)
		workbook.save('Excel_Workbook.xls')
		row+=1
	except (ConnectionError, TimeoutError) as e:
		print(e)
	except ConnectionResetError:
		continue
		
   
	    

   
#for i in filtered_url:
#print(i)
#print(i)
