from HTMLParser import HTMLParser

class OctoBearParser(HTMLParser):
    _foundForm = False
    _foundInput = False
    _parseInner = False
    
    forms = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'form':
            self._foundForm = True
            self.forms.append(dict())
            i = len(self.forms) - 1
            print 'i=', i
            for attr in attrs:
                key = attr[0]
                val = attr[1]
                self.forms[i][key] = val
            return
            
        if tag == 'input' and self._foundForm:
            i = len(self.forms) - 1
            if tag not in self.forms[i]:
                self.forms[i][tag] = []
            self.forms[i][tag].append(attrs)
            
    def handle_data(self, data):
        return
        
    def handle_endtag(self, tag):
        if tag == 'form':
            self._foundForm = False
    
    def feed(self, data):
        if type(data) is bytes:
            data = str(data)
        data = data.replace('\n', '')
        data = data.replace('\r', '')
        HTMLParser.feed(self, data)

