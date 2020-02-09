#!/usr/bin/env python3

#Import modules###################################################################################################################################################################################################
import requests, re, time, sys, os, calendar, logging
with open('main.log', 'w'):
    pass
logging.basicConfig(filename='main.log',format='%(levelname)s:%(filename)s:line %(lineno)d:  %(message)s', level=logging.DEBUG)
logging.addLevelName(60,'URL-UPDATE')
logging.addLevelName(70,'DEPTH-CHANGE')
logging.info("Initiated program")
requests.encoding = 'ISO-8859-1'

#Get the base URL###################################################################################################################################################################################################
baseinitial = input('URL:   https://')
if baseinitial[len(baseinitial)-1] != '/':
  print(' -  Added a trailing slash to URL\n')
  baseinitial = baseinitial + '/'

#Get the max number of links per page###################################################################################################################################################################################################
try:
  maxlinks = int(input('Max number of links per page to look at: (press enter for no restriction)'))
except:
  maxlinks = 'No Restriction'

#Define variables###################################################################################################################################################################################################
startime = calendar.timegm(time.gmtime())
baseurl = 'https://' + baseinitial
sleep = 0
sizes = []
nnn = baseinitial
upp = []
au = []
errors = []
words = ''
fc = open('fc','w+')
fc.write('```mermaid\ngraph LR\n')
subs = {}
tab = 0
maxdepth = int(input('What should the maximum depth be?'))-1#1
amo = 0
allurls = []

#File setup###################################################################################################################################################################################################
try: 
  os.mkdir('./temp/')
except:
  print('Overwriting ./temp/')
w = open('./temp/urls','w+')
f = open('./temp/words','w+')
fc = open('./temp/fc','w+')
fc.write('```mermaid\ngraph LR\n')

#Page class###################################################################################################################################################################################################
class Page():
  def __init__(self,url):
    logging.log(60,'Started gathering for {}.'.format(url))
    try:
      with requests.get(url) as p:
        if p.status_code != 200:
          logging.warning('When looking at {}, found response code {} instead of 200.'.format(url,p.status_code))
          self.content = 'invalid response code'
        elif p.headers['content-type'].split(';')[0] != 'text/html':
          logging.warning('When looking at {}, found content type {} instead of text/html.'.format(url,p.headers['content-type'].split(';')[0]))
          self.content = 'invalid content type'          
        else:
          self.response = p
          try:
            self.encoding = p.headers['content-type'].split(';')[1]
          except:
            self.encoding = 'Not Provided'
          self.content = str(p.content)#.decode('utf-8')
    except requests.exceptions.ConnectionError:
      logging.warning('Could not find server for {}.'.format(url))
    self.url = url
    try:
      self.title = re.findall('(?<=<title>)(.*)(?=<\/title>)',self.content)[0]
    except:
      self.title = self.url[0:20]
    try:
      self.domain = 'https://' + re.findall('(?<=://)(.*)(?=/)',url)[0]
    except IndexError:
      self.domain = url
    logging.log(60,'Finished gathering for {}.'.format(url))

  def getURLS(self):
    l = re.findall('(?<=href=\")(.*?)(?=\")',self.content)
    l = l + re.findall('(?<=href=\')(.*?)(?=\')',self.content)
    return l

#Function definitions###################################################################################################################################################################################################
def tabify():
  global tab
  c = ''
  if True:
    for x in range(tab):
      c = c + '|   '
  return c
def makeAbsolute(urls,domain,base):
  fi = []
  for y in urls:
    try:
      x = re.findall('(?<=)(.*)(?=\?)',y)[0]
    except:
      x = y
    if x == '':
      continue
    elif '*' in x:
      continue
    elif ('<' in x) or ('>' in x):
      continue
    elif x[0] == '.':
      continue
    elif x[0:2] == '//':
      fi.append('https:' + x)
    elif x[0] == '/':
      fi.append(domain + '/' + x)
    elif x[0:2] == 'ht':
      fi.append(x)
    elif x[0] == '<':
      continue
    elif x[0] == ' ':
      continue
    else:
      fi.append(base + '/' + x)
  for x in range(len(fi)):
    try:
      if fi[x][0] != 'h':
        del fi[x]
      if ('{' in fi[x])or('}' in fi[x]):
        del fi[x]
    except:
      print(end='')
  return fi
#Mainloop###################################################################################################################################################################################################
def main(base):
  global words
  global tab
  global au
  global maxdepth
  global w
  global f
  global fc
  global sleep
  global amo
  global maxlinks
  global allurls
  page = Page(base)
  amo = amo + 1
  page.domain
  logging.info('Start get URLS for ' + base)
  urls = makeAbsolute(page.getURLS(),page.domain,base)
  for x in re.findall('>.*?<',page.content):
    words = words + ' ' + x.replace('>','').replace('<','')
  upp.append(len(urls))
  if maxlinks != 'No Restriction':
    urls = urls[0:maxlinks]
  for x in range(len(urls)):
    try:
      if urls[x][0] != 'h':
        del urls[x]
      if ('{' in urls[x])or('}' in urls[x]):
        del urls[x]
    except:
      print(end='')
    au.append(x)
  logging.info('End get URLS for ' + base)
  if tab < maxdepth+1:
    for x in range(len(urls)):
      #print(amo)
      try:
        subs[tab].append('' + urls[x] + '' + '\n')
      except KeyError:
        subs[tab] = []
        subs[tab].append('' + urls[x] + '' + '\n')
      fc.write(base + '-->' + urls[x] + '\n')
      if tab == 0:
        if x+1 == len(urls):
          print('└──' + str(x+1) + '/' + str(len(urls)))
          w.write('└──' + urls[x] + '\n')
        else:
          print('├──' + str(x+1) + '/' + str(len(urls)))
          w.write('├──' + urls[x] + '\n')
      elif x+1 != len(urls):
        print(tabify() + '├──' + str(x+1) + '/' + str(len(urls)))
        w.write(tabify() + '├──' + urls[x] + '\n')
      else:
        print(tabify() + '└──' + str(x+1) + '/' + str(len(urls)))
        w.write(tabify() + '└──' + urls[x] + '\n')
      time.sleep(sleep)
      tab = tab + 1
      logging.log(70,'Changed by +1. From {} to {}.'.format(tab-1,tab))
      try:
        if urls[x] not in allurls:
          allurls.append(urls[x])
          main(urls[x])
      except KeyboardInterrupt:
        print('user abort')
        logging.debug('USER ABORT FOR ' + urls[x])
      tab = tab - 1
      logging.log(70,'Changed by -1. From {} to {}.'.format(tab+1,tab))

    
goodwords = []
totals = {}
fl = []




print(baseurl)
w.write(baseurl + '\n')
main(baseurl)



for x in words.split():
  if not re.search('[/,_,;,\\,\',\\n,\=,\[\],0-9,!@#$%^&*(),.?":{}|<>,\-]',x):
    goodwords.append(x.lower())

for x in goodwords:
  totals[x] = 0
for x in goodwords:
  totals[x] = totals[x] + 1
#print(totals)
ml = 0
for x in totals.keys():
  if (len(str(int(totals[x])))) > ml:
    ml = len(str(int(totals[x])))
#print(ml)





for x in totals.keys():
  tb = ''
  for y in range(ml-len(str(totals[x]))):
    tb = tb + '0'
  tb = tb + str(totals[str(x)]) + '     ' + str(x)
  fl.append(tb)
fl.sort(reverse=True)
#print(fl)
for x in fl:
  f.write(x + '\n')

print('\n\n\n\n\n\n\n\n\Gathered about ' + str(amo) + ' pages, at depth ' + str(1) + '. The base url was ' + baseurl + '.')
if len(errors) != 0:
  print('\nSome errors occured: ' + str(errors))
else:
  print('\nNo errors occured.')

fc.write('subgraph Depth 0\n' + baseurl + '\nend\n')

for x in subs.keys():
  fc.write('subgraph Depth ' + str(x+1) + '\n')
  for z in subs[x]:
    fc.write(z + '')
  fc.write('end\n')

fc.write('```')
fc.close()
f.close()
w.close()
os.chdir('/home/runner/sci/')

#print('Flowchart File Size: {} bytes'.format(os.path.getsize('./temp/fc')))
#print('Words Ranking Size: {} bytes'.format(os.path.getsize('./temp/words')))
#print('URLS List Size: {} bytes'.format(os.path.getsize('./temp/urls')))
g = 0
for x in upp:
  g = g + x
print('Average URLS per page: {}'.format(g/len(upp)))

endtime = calendar.timegm(time.gmtime())

open('./temp/meta','w+').write('Base URL: ' + baseinitial + '\nTime: ' + str(endtime-startime) + ' seconds\n' + str(len(errors)) + ' errors\nDepth: ' + str(maxdepth+2) + '\n# of Pages: ' + str(amo) + '\nMax links per page: ' + str(maxlinks) + '\nFlowchart File Size: {} bytes\n'.format(os.path.getsize('./temp/fc')) + 'Word Ranking File Size: {} bytes\n'.format(os.path.getsize('./temp/words')) + 'URLS List File Size: {} bytes\n'.format(os.path.getsize('./temp/urls')))
os.system('tar cf ' + nnn.replace('.com/','').replace('/','') + '@' + str(maxdepth+1) + '.scrap fc meta urls words')

input('Press enter to clear temporary files.')
os.system('rm fc meta urls words tempfile')
print(allurls)