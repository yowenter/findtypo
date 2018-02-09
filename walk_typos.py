# -*-encoding :utf-8 -*-

import re
import os
import typo_checker


def tokenize(text):
    return re.findall(r"([\w ]{30,})",text)

    


def tokenize_file(fpath):
    if not fpath.endswith("md"):
        return 
    with open(fpath, 'r') as f:
        text = f.read()
        return tokenize(text)



def main():
    directory = "/Users/wenter/dao-repos/commiter/metrics"
    typo_checker.load_white_word_list()
    for root,_,flist in os.walk(directory):
        
        for f in flist:
            fpath = os.path.join(root,f)
            if "vendor" in fpath:
                continue

            tokens = tokenize_file(fpath)
            if not tokens:
                continue
            print "#########"*10
            print fpath
            for token in tokens:
                 m = typo_checker.find_all_possible_in_text(token)
                 for _ in m:
                     print _


        
main()
