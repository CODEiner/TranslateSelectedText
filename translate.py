import sublime, sublime_plugin
import json
from urllib2 import urlopen
from urllib import urlencode

class translateSelectedCommand(sublime_plugin.TextCommand):

    def getTranslate(self, lang1, lang2, text):

        base_url = 'http://ajax.googleapis.com/ajax/services/language/translate?'
        
        params = urlencode({
            'v': 1.0,
            'q': text.encode('utf-8'),
            'langpair': '%s|%s' % (lang1, lang2),
        })
        url = base_url+params

        try:
            content = urlopen(url).read()
            js = json.loads(content)
            translation = js['responseData']['translatedText']
        except:
            #print js['responseDetails']
            print 'translate error'
            translation = text

        return translation

    def run(self, edit, from_language="", to_language="en"):
        for region in self.view.sel():
            text = self.getTranslate(from_language, to_language, self.view.substr(region))
            self.view.erase(edit, region)
            self.view.insert(edit, region.begin(), text)