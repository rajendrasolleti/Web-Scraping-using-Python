import sys
import bs4
from bs4 import BeautifulSoup
import time
import re

def login(username,password) :   
   driver.get("************")#Masked
   driver.find_element_by_xpath("//*[@id=\"loginMessage\"]/a").click()
   usernameelement = driver.find_element_by_id('userNameInput')
   usernameelement.send_keys(username)
   pwd = driver.find_element_by_id('passwordInput')
   pwd.send_keys(password)
   driver.find_element_by_id("submitButton").click()

def extractcontent(url):   
   driver.get(url)
   soup= BeautifulSoup(driver.page_source,'lxml')
   [s.extract() for s in soup('iframe')]
   [s.extract() for s in soup('script')]
   [s.extract() for s in soup('style')]   
   content = soup.get_text()
   content = re.sub('<[^>]*>','',content)
   content = cleantext(content)
   sentences = set(content.split('\n'))   
   file=open(filename,'a',encoding='utf-8')
   file.write('\n/******FILE URL: ' + url + '*******/\n')
   for sentence in sentences:
      if len(sentence)>35:
         file.write(sentence+'\n')
   file.close()
   return

def cleantext(content):
   while (content.find('\n\n')>0):
      content = content.replace('\n\n','\n')
   while (content.find('  ')>0):
      content = content.replace('  ',' ')
   return content

def extracturls(url):
   allurls = []
   try:
      driver.get(url)
      soup= BeautifulSoup(driver.page_source,'lxml')
      [s.extract() for s in soup('iframe')]
      [s.extract() for s in soup('script')]
      [s.extract() for s in soup('style')]      	
      links = soup.find_all('a', href=True)
      for a in links:
         if 'http' in a['href']:
            allurls.append(a['href'])
      return list(set(allurls))
   except:
      return allurls

if len(sys.argv) == 6:
   url = sys.argv[1]
   depth = int(sys.argv[2])
   filename = str(sys.argv[3])
   username = str(sys.argv[4])
   password = str(sys.argv[5])
else:
   url = '********************************'#Masked
   depth = 1
   filename = r'D:\test.html'   


from selenium import webdriver
driver = webdriver.Chrome('D:\chromedriver.exe')
login(username,password)
time.sleep(10)
AllLinks = extracturls(url)
if(depth==1):
   for link in AllLinks:
      extractcontent(link)
else:
   AllLinksMultiDimensional=[]
   index=1
   while depth>1:
      depth = depth-1
      AllLinksMultiDimensional.append([])
      AllLinksMultiDimensional[0].extend(AllLinks)
      AllLinksMultiDimensional.append([])
      for link in AllLinksMultiDimensional[index-1]:         
         AllLinksMultiDimensional[index-1].extend(extracturls(link))
      AllLinks.extend(AllLinksMultiDimensional[index-1])
      index = index+1 
   AllLinks = set(AllLinks)
   file=open(filename,'a',encoding='utf-8')
   for link in AllLinks:
      file.write(link + '\n')
      file.close()
      extractcontent(link)
