import sublime, sublime_plugin
import httplib
import urllib


class translateSelectedCommand(sublime_plugin.TextCommand):

    def getTranslate(self, text):

        if(text == text.encode('utf-8')):
            lang1, lang2 = ('en', 'ru')
        else:
            lang1, lang2 = ('ru', 'en')

        params = urllib.urlencode({
            'text': text.encode('utf-8'),
            'sl': lang1,
            'tl': lang2,
        })
        headers = {'User-Agent': 'Mozilla/5.0',
                   'Referer': 'http://slovari.yandex.ru/~translate/',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Accept-Charset': 'utf-8',
                  }
        try:
            conn = httplib.HTTPConnection('slovari.yandex.ru')
            conn.request("POST", '/async/translator.xml', params, headers)
            response = conn.getresponse()
        except:
            sublime.status_message('translate ERROR :(')
        
        if(response.status == 200):
            content = response.read()
            text = content.decode('utf-8')
        else:
            sublime.status_message('Translate ERROR: %s %s'%(response.status, response.reason))
        
        return text


    def run(self, edit):
        for region in self.view.sel():
            text = self.getTranslate(self.view.substr(region))
            self.view.replace(edit, region, text)

