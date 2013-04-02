from bs4 import BeautifulSoup
import urllib2



'''
Returns a list of the forms as dict objects
Dependancy: BeautifulSoup
Usage:
    forms = pack_forms('http://www.sungjkang.com/~lna/')

    for form in forms:
        for key, val in form.items():
            print key, val, '\n'

'''
def pack_forms(url):
    page = urllib2.urlopen(url)
    formatted = ''
    for i in page:
        formatted += i
    page = formatted.lower()
    soup = BeautifulSoup(page)

    forms = []

    for form in soup.findAll('form'):
        forms.append(dict())
        i = len(forms) - 1
        forms[i]['action'] = form.get('action', None)
        forms[i]['method'] = form.get('method', None)
        input_fields = form.findAll('input')
        forms[i]['input'] = []
        for input_field in input_fields:
            #print item, '\n'
            temp = dict()
            temp['name'] = input_field.get('name', None)
            temp['id'] = input_field.get('id', None)
            temp['value'] = input_field.get('value', None)
            temp['class'] = input_field.get('class', None)
            temp['type'] = input_field.get('type', None)
            forms[i]['input'].append(temp)
            
            
    return forms
    
    
    
    

