import re

def tabify():
  global tab
  c = ''
  if True:
    for x in range(tab):
      c = c + '|   '  
  return c
def makeAbsolute(urls):
  global domain, base
  fi = []
  for y in urls:
    y.replace('//','/')
    y.replace(':/','://')
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
    finally:
      print(end='')
  return fi