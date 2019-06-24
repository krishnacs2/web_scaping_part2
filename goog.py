#https://github.com/MarioVilas/googlesearch
class Gsearch_python:
   def __init__(self,name_search):
      self.name = name_search
   def Gsearch(self):
      count = 0
      try :
         from googlesearch import search
      except ImportError:
         print("No Module named 'google' Found")
      for i in search(query=self.name,tld='com',lang='en',num=10,stop=10,pause=10):
         count += 1
         print (count)
         print(i + '\n')
if __name__=='__main__':
   gs = Gsearch_python("Revanth\"Reddy\"")
   gs.Gsearch()