import urllib , cStringIO
import urllib2
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import mechanize
from PIL import Image


br = mechanize.Browser()
uri = 'http://students.gtu.ac.in/StudHist.aspx'

br.open(uri)  
html = br.response().read()
soup = BeautifulSoup(html,"lxml")
img1 = soup.find_all('img')
file = cStringIO.StringIO(urllib.urlopen("http://students.gtu.ac.in/"+img1[1]['src']).read())
img = Image.open(file)
img.show()

viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']


#the http headers are useful to simulate a particular browser (some sites deny
#access to non-browsers (bots, etc.)
#also needed to pass the content type. 
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# we group the form fields and their values in a list (any
# iterable, actually) of name-value tuples.  This helps
# with clarity and also makes it easy to later encoding of them.
cap_val = raw_input("Enter Captcha ")
formFields = (
   # the viewstate is actualy 800+ characters in length! I truncated it
   # for this sample code.  It can be lifted from the first page
   # obtained from the site.  It may be ok to hardcode this value, or
   # it may have to be refreshed each time / each day, by essentially
   # running an extra page request and parse, for this specific value.
  
   # following are more of these ASP form fields
   (r'__VIEWSTATE', viewstate),
   (r'__EVENTVALIDATION',eventvalidation),
   (r'__EVENTTARGET',r''),
   (r'__EVENTARGUMENT',r''),

   #but then we come to fields of interest: the search
   #criteria the collections to search from etc.
                                                      # Check boxes  
   (r'ctl00$MainContent$btnSubmit', 'Submit'),  # file number
   (r'ctl00$MainContent$txtEnrollNo', '130750116023'),  # file number
   (r'ctl00$MainContent$CodeNumberTextBox', cap_val),  # Legislative text
   
)

# these have to be encoded    
encodedFields = urllib.urlencode(formFields)

req = urllib2.Request(uri, encodedFields, headers)
f= urllib2.urlopen(req)     #that's the actual call to the http site.

# *** here would normally be the in-memory parsing of f 
#     contents, but instead I store this to file
#     this is useful during design, allowing to have a
#     sample of what is to be parsed in a text editor, for analysis.

 
soup = BeautifulSoup(f,"lxml")
all_data = soup.find_all("table")


if len(all_data) == 3:
  print "Sorry Incorrect Enroll No"
  exit()


## Information Table
 info_data = all_data[4].findAll('td') 
info_table= PrettyTable(['++++','Student Detail'])
for i in range(0,8,2):
  info_table.add_row([info_data[i].get_text().strip(),info_data[i+1].get_text().strip()])

print info_table


## Backlog Table

bck_sem_info = all_data[5].findAll('th')
bck_info = all_data[5].findAll('td')

bck_table= PrettyTable(['++++','++'])

for n,i in enumerate(bck_sem_info): 
        bck_table.add_row([bck_sem_info[n].get_text(),bck_info[n].get_text() ])

print bck_table