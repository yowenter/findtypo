# -*-encoding :utf-8 -*-

import re
import os
import datetime
import typo_checker
import traceback

regexp_f = re.compile(".*\.(md|go)")

def tokenize(text):
    return re.findall(r"([\w ]{30,})",text)

    


def tokenize_file(fpath):
    with open(fpath, 'r') as f:
        text = f.read()
        return tokenize(text)


class Pipe(object):
    def __init__(self, directory, fname):
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        self.buffer = []
        self.directory = directory
        self.fname = fname
        with open(os.path.join(self.directory, self.fname),'w') as f:
            f.write("{}".format(datetime.datetime.now()))
    
    def write(self,s):
        self.buffer.append(s)
    
    def flush(self):
        self.save()
        self.buffer = []
    
    def save(self):
        with open(os.path.join(self.directory, self.fname), "a") as f :
            for b in self.buffer:
                f.write(b)
                f.write("\n")


        


def main():
    directory = "/Users/wenter/private-repos/website"
    save_directory = "/Users/wenter/Desktop/tmp"
    typo_checker.load_white_word_list()
    pipes = dict()

    i =0 
    for root,_,flist in os.walk(directory):
        
        for f in flist:
            if not regexp_f.match(f):
                continue
            i+=1
            if i%30==0:
                    for p in pipes:
                        pipes[p].flush()

            fpath = os.path.join(root,f)
            if "vendor" in fpath:
                continue

            tokens = tokenize_file(fpath)
            if not tokens:
                continue
            print "#########"*10
            print "Loading",fpath
            for token in tokens:
                try:
                    matches = typo_checker.find_all_possible_in_text(token)
                except Exception as e :
                    print traceback.format_exception()
                    

                for m in matches:
                     issue_type = m.rule.issueType
                     pipe = pipes.get(issue_type)
                     if not pipe:
                         pipe = Pipe(save_directory, "{}.txt".format(issue_type))
                         pipes[issue_type] = pipe
                
                     pipe.write("[{}]: {} -> {}".format(fpath[len(directory):], m.context.text, m.replacements[:1]))

     
    for p in pipes:
        pipes[p].save()


        
main()
