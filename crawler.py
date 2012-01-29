import requests
from BeautifulSoup import BeautifulSoup
from pprint import pprint

g = open('out.csv', 'w')
url = 'http://campion.edu.ro/arhiva/index.php?page=problems&action=view&id=0&ordercriteria=difficulty&ordertype=desc&filtercriteria=all&filterid=0&paging=';
default_url = 'http://campion.edu.ro/arhiva/'

def crawl():
	for i in range(1,88):
		print 'Starting page {0}'.format(i)
		r = requests.get(url + str(i))
		
		page = r.content
		soup = BeautifulSoup(page)

		table = soup.find('table', {'class' : 'tabel', 'cellpadding':'2','cellspacing':'0'})
		parse(table.prettify())

def myPrint(obj):
	if isinstance(obj, str):
		g.write(obj.strip())
	else:
		g.write(obj.string.strip().encode('utf-8'))
	g.write(',')

def parse(table):
	soup = BeautifulSoup(table)
	rows = soup.findAll('tr')
	for row in rows[1:]:
		columns = row.findAll('td')
		for i in range(len(columns)):
			if i==0:
				myPrint(columns[i])
			elif i==1:
				myPrint(columns[i].strong)
			elif i==2:
				myPrint(columns[i].a)
			elif i==3:
				if len(columns[i]) == 3:
					myPrint(columns[i].a)
				else:
					myPrint("")
			elif i==4:
				if str(columns[i]).find('mic') != -1:
					myPrint('1')
				elif str(columns[i]).find('med') != -1:
					myPrint('2')
				else:
					myPrint('3')
			else:
				img = columns[i].findAll('img')
				myPrint(str(len(img)))
		# And link
		myPrint(default_url + str(columns[1].a['href']))
		g.write('\n')
		print 'done {0}'.format(str(columns[0].string).strip())
		# print(column[1].strong.string.strip())


# MAIN
g.write('ID,Nume,Concurs,Profesor,grupa,dificultate,URL\n')
crawl()
print('Finished :-)')
