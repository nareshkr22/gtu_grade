import urllib , cStringIO
import urllib2
from prettytable import PrettyTable
from bs4 import BeautifulSoup
import mechanize
from PIL import Image



enroll = int(raw_input("Enter The enrollment no : "))
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
   (r'ctl00$MainContent$txtEnrollNo', enroll),  # file number
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
 
if len(all_data) == 4:
  print "Sorry  Something went wrong"
  quit()


## Information Table
info_data = all_data[4].findAll('td') 
info_table= PrettyTable(['++++','Student Detail'])
for i in range(0,8,2):
  info_table.add_row([info_data[i].get_text().strip(),info_data[i+1].get_text().strip()])

print info_table


## Backlog Table

bck_sem_info = all_data[5].findAll('th')
bck_info = all_data[5].findAll('td')

bck_table= PrettyTable()

for n,i in enumerate(bck_sem_info): 
        bck_table.add_column(bck_sem_info[n].get_text(),[bck_info[n].get_text()])
       
print bck_table


## Sem Info
sem = soup.find_all("table", { "class" : "mrksheet Mytable" })


sem_val = int(raw_input("Enter the semster"))
if sem_val > len(sem)+1:
  print "Sorrry"
  quit()
else:  
  next_child = sem[sem_val-1].find_next_sibling("table")
  #print next_child 
  print "sem = " + str(sem_val)
  try :
      while next_child.get('class',[])[0] != "mrksheet":  
          if next_child.get('class',[])[0] == "mrksheet":
              break
          else:        
              
              sem_info = next_child.findAll('tr') 
              
              sem_headers = next_child.findAll('th')         
              sem_headers = [j.get_text().strip() for j in sem_headers]
              
              sem_info = next_child.findAll('td') 
              sem_info = [j.get_text().strip() for j in sem_info]
              
              if next_child.get('class',[])[0] == "Session":
                  print "Examination Type" 
                  for i in sem_info: print i.strip()
          
              if next_child.get('class',[])[0] == "mrksheetdetail":
                  sem_t = PrettyTable(sem_headers)
                  size = len(sem_info)/len(sem_headers)
                  o = 0
                  p = len(sem_headers)
                  while p <= len(sem_info):               
                      sem_t.add_row(sem_info[o:p])
                      o = o+ len(sem_headers)
                      p = p+ len(sem_headers)
                  print sem_t
              next_child = next_child.find_next_sibling("table")
  except:
          print "Thank You very Much for using the program"
  
