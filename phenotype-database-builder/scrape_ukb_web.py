'''
This script will scrape the UKB online showcase and print data-fields, their descriptions along with the type of variable they correspond to, i.e., Integer, Categorical, Continuous, etc.
'''

import bs4 as bs
from urllib2 import urlopen
import unicodedata

sauce = urlopen('http://biobank.ctsu.ox.ac.uk/crystal/list.cgi').read()
soup = bs.BeautifulSoup(sauce, 'lxml')

field_listing = ['Integer',
		'Categorical (single)',
		'Categorical (multiple)',
		'Continuous',
		'Text',
		'Date',
		'Time',
		'Compound']

df_descriptions = []

for url in soup.find_all('a'):
	if url.text in field_listing:
		df_type = url.text
		link = 'http://biobank.ctsu.ox.ac.uk/crystal/' +  url.get('href')
		sauce_loop = urlopen(link).read()
		soup_loop = bs.BeautifulSoup(sauce_loop, 'lxml')
		raw_text = unicodedata.normalize("NFKD", soup_loop.get_text('\t'))
		lines = raw_text.split('\n')
		for line in lines:
			splt = [s for s in line.split('\t')[1:] if s != '' 
							and s != ' ' 
							and s!= '  ' 
							and s!= u'\u2020'] 
							#u'\u2020' is the dagger from Compound
			if len(splt) == 3 and splt[0].isdigit():
				splt.append(df_type)
				df_descriptions.append('%s\t%s\t%s\t%s'%(splt[0], splt[1], splt[2], splt[3]))

if __name__ == "__main__":
	for f in df_descriptions:
		#print '%s\t%s\t%s\t%s'%(f[0],f[1],f[2],f[3])
		print f
