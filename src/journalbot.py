from BeautifulSoup import BeautifulSoup
import urllib2
import simplejson

def getJourn(base,uri):
	url=base+uri
	print url
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	boxes=soup.findAll('input',{'class':'gca-checkbox'})
	queryString='/gca?submit=Get+All+Checked+Abstracts'
	for box in boxes:
	    queryString+='&gca='+box['value']
	
	print queryString
	return base+queryString
	
def getAbstracts(url,conf):
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	temp=conf.pop('container')
	abstracts=soup.findAll(temp.keys()[0],{temp.values()[0].keys()[0]:temp.values()[0].values()[0]})
	i=0
	a=[]
	for abstract in abstracts:
		print i
		confIt=conf.copy()
		a.append({})
		a[i]['soup']=abstract
		a[i]['journal']=confIt.pop('journal')
		a[i]['journ']=confIt.pop('journ')
		a[i]['url']=url
		a[i]['conf']=confIt
		for key,value in confIt.items():
			if(type(value)==type('')):
				a[i][key]=abstract.find(value).text
			elif(type(value)==type({})):
				if(len(value)==1):
					a[i][key]=abstract.find(value.keys()[0],{value.values()[0].keys()[0]:value.values()[0].values()[0]}).text
				elif(len(value)==2):
					if(value.keys()[1]=='tag'):
						a[i][key]=abstract.find(value.keys()[0],{value.values()[0].keys()[0]:value.values()[0].values()[0]}).find(value.values()[1]).text
					elif(value.keys()[1]=='property'):
						a[i][key]=abstract.find(value.keys()[0],{value.values()[0].keys()[0]:value.values()[0].values()[0]})[value.values()[1]]
		
		i+=1

	print len(a),'abstracts scraped'
	return a
	
def writeFiles(a,fName="output"):
	with open(fName+".html", "a") as myfile:
		for abstract in a:
		    myfile.write(abstract['soup'].prettify())
		    
	with open(fName+".txt","a") as myfile2:
		for abstract in a:
			myfile2.write(abstract['title'].encode('UTF-8'))
			myfile2.write('\n------\n')
			myfile2.write(abstract['text'].encode('UTF-8'))
			myfile2.write('\n------\n')
			myfile2.write(abstract['url'].encode('UTF-8'))
			myfile2.write('\n------\n')
			myfile2.write('\n------\n')
	
if __name__ == '__main__':
	base="http://www.jneurosci.org"
	uri="/content/current"
	f=open('../res/journals.json')
	conf=simplejson.load(f)
	query=getJourn(base,uri)
	a=getAbstracts(query,conf)
	writeFiles(a)
	
