# -*-encoding :utf-8 -*-

import requests
import os

LANGUAGE_TOOL_API = "http://localhost:8081/v2/check"

# Download LanguageTool from `https://languagetool.org/`
# Up LanguageTool  `java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081`



def check_text(text, language='en-US'):
    resp = requests.get(LANGUAGE_TOOL_API,params={"language":language, "text":text}, timeout=3)
    return resp.json()





class Model(object):
    attrs = dict()

    def __init__(self, **kwargs):
        self.data = dict()
        for k in kwargs:
            if k in self.attrs :
                self.data[k] = kwargs[k]
                
    def __getattr__(self, attr):
        if attr not in self.attrs:
            return None
        return self.data.get(attr)
    

    @classmethod
    def from_data(cls, data):
        m = cls(**data)
        return m

    def __repr__(self):
        return str(self.data)


class Match(Model):
    attrs = {
        "message":str,
        "replacements":list,
        "rule":object,
        "sentence":str,
        "context": object
    }

class Context(Model):
    attrs = {
        "offset":int,
        "text":str,
        "length":int
    }
class Rule(Model):
    attrs = {
        "id":str,
        "description":str,
        "issueType":str,
        "category":object
    }

class Replacement(Model):
    attrs = {
        "value":str
    }

    def __repr__(self):
        return self.value



def iterate_model(match_data):
    if not match_data:
        return None

    M = None 
    for model in [Match, Rule, Replacement,Context]:
        if len([k for k in model.attrs.keys() if k in match_data.keys()]) == len(model.attrs.keys()):
            M = model.from_data(match_data)
            for k in model.attrs:
                if model.attrs[k] == list:
                    M.data[k] = [iterate_model(v) for v in getattr(M,k)]
                elif model.attrs[k] == object:
                    M.data[k] = iterate_model(getattr(M,k))
    
    if M is None:
        return match_data
    
    return M
        



white_word_list = set()

def load_white_word_list():
    if not os.path.exists("white_word.list"):
        print "White word list file not found"
    with open("white_word.list","r") as f:
        for line in f:
            white_word_list.add(line.strip())





typo_found = []
def find_typo_in_text(text):
    result = check_text(text)
    matched = result.get("matches")
    matches = [iterate_model(m) for m in matched]
    for m in matches:
        word = m.context.text[m.context.offset:m.context.offset+m.context.length].lower()
        if m.rule.issueType == "misspelling"  and word not in typo_found and word not in white_word_list:
            typo_found.append(word )
            yield "{}: {} -> {}".format(m.rule.issueType, word, m.replacements[:1])


def find_all_possible_in_text(text):
    result = check_text(text)
    matched = result.get("matches")
    matches = [iterate_model(m) for m in matched]
    for m in matches:
        yield "{}: {} -> {}".format(m.rule.issueType, m.context.text, m.replacements[:1])
