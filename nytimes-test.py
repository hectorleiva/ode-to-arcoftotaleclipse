#!/usr/local/bin/python
import requests, os

directory = './newspapers/'
newspaper = 'nytimes.com'

if not os.path.exists(directory):
    os.makedirs(directory)

res = requests.get('http://' + newspaper)
res.raise_for_status()

paper = open(directory + newspaper + '.html', 'wb')
for chunk in res.iter_content(100000):
    paper.write(chunk)
paper.close()
