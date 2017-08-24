import urllib , cStringIO
import urllib2
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
   (r'ctl00$MainContent$txtEnrollNo', '130df750116023'),  # file number
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

try:
  fout = open('tmp.htm', 'w')
except:
  print('Could not open output file\n')

fout.writelines(f.readlines())

fout.close()

hd = open("tmp.htm","r").read()
soup = BeautifulSoup(hd,"lxml")

ldata = soup.find_all("table")
msg = """<html><head> <title>Codelancer</title> <meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="author" content="Naresh Kumar"><meta name="description" content="The best thing about a boolean is even if you are wrong, you are only off by a bit."><meta name="keywords" content="naresh, kumar, naresh kumar, codelancers , IT services, business solutions, consulting, web design, web development, ui/ux, android app development, marketing, web hosting, social media marketing,s"><meta name="twitter:card" content="summary"><meta name="twitter:site" content="Codelancers"><meta name="twitter:creator" content="Naresh Kumar"><meta name="twitter:title" content="Codelancers"><meta name="twitter:description" content="The best thing about a boolean is even if you are wrong, you are only off by a bit."> <meta name="twitter:image" content="http://www.codelancers.in/image.jpg"><meta property="og:title" content="Codelancers" /><meta property="og:url" content="http://www.codelancers.in/" /><meta property="og:image" content="http://www.codelancers.in/image.jpg"/><meta property="og:site_name" content="Naresh Kumar" /><meta property="og:description" content="The best thing about a boolean is even if you are wrong, you are only off by a bit." /><!--[if IE]><meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'><![endif]--><!-- mobile viewport optimized --><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" /><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"><!-- Optional theme --><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous"><script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script> <!-- Latest compiled and minified JavaScript --><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script></head>"""
print ldata

with open('sample.html','w') as mf:
  mf.write(msg)
  get_class = ldata[4].get('class')
  ldata[4]['class'] = ldata[4].get('class',[])+['table table-bordered']
  mf.write(str(ldata[4]))
  for e in ldata[5:]:
    mf.write('<div class="table-responsive">')
    get_class = e.get('class')
    if get_class:
      if get_class[0] == "mrksheetdetail" or get_class[0] == "Mytable" or get_class[0] == "textcenter":
        e['class'] = e.get('class',[])+['table table-striped']
        mf.write(str(e))
      else:
        mf.write(str(e))
    
      
    
    mf.write('</div>')
