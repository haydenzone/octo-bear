from bs4 import BeautifulSoup
import requests

'''
Class: OctoBearFormHanlder
Dependancy: BeautifulSoup
            requests

'''
class OctoBearFormHandler:
    
    def __init__(self, url):
        self._url = url
        self.__initForms()    
                
                

    def __initForms(self):
        r = requests.get(self._url)
        soup = BeautifulSoup(r.text.lower())

        self.forms = []

        for form in soup.findAll('form'):
            self.forms.append(dict())
            i = len(self.forms) - 1
            self.forms[i]['action'] = form.get('action', None)
            self.forms[i]['method'] = form.get('method', None)
            input_fields = form.findAll('input')
            self.forms[i]['input'] = []
            for input_field in input_fields:
                #print item, '\n'
                temp = dict()
                temp['name'] = input_field.get('name', None)
                temp['id'] = input_field.get('id', None)
                temp['value'] = input_field.get('value', None)
                temp['class'] = input_field.get('class', None)
                temp['type'] = input_field.get('type', None)
                self.forms[i]['input'].append(temp)
        
        
    def setURL(self, url):
        self._url = url
        self.__initForms()
    
    def getURL(self):
        return self._url

    '''
    Returns a list of the forms as dict objects
    Usage:
        forms = getForms()

        for form in forms:
            for key, val in form.items():
                print key, val, '\n'

    '''
    def getForms(self):
        return self.forms
        
        
    '''
    Goes through each form item and attempts to send a request to
    the action URL
    '''
    def sendRequest(self, action, payload):
        if self.forms is None:
            return
        
        r = requests.post(self._url + '/' + action, data = payload)
        
