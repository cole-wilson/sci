import os
try:
  os.mkdir('temporary')
except:
  print('Overwriting files in ./temporary')
finally:
  w = open('./temporary/urls','w+')
  f = open('./temporary/words','w+')
  fc = open('./temporary/fc','w+')
  fc.write('```mermaid\ngraph LR\n')

