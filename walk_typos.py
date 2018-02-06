# -*-encoding :utf-8 -*-

import re
import os
import typo_checker


def tokenize(text):
    return re.findall(r"([\w ]{20,100})",text)

    


def tokenize_file(fpath):
    if not fpath.endswith("md"):
        return 
    with open(fpath, 'r') as f:
        text = f.read()
        return tokenize(text)



def main():
    directory = ""
    for root,_,flist in os.walk(directory):
        if len(_)>=1:
            continue
        for f in flist:
            fpath = os.path.join(root,f)
            tokens = tokenize_file(fpath)
            if not tokens:
                continue
            print "#########"*10
            print fpath
            for token in tokens:
                 m = typo_checker.find_typo_in_text(token)
                 for _ in m:
                     print _


        
main()
