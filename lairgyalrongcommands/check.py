"""
Compute partial cognates and alignments and create a wordlist.
"""

from lingpy import *
from sinopy import segments
from lexibank_lairgyalrong import Dataset
from pylexibank import progressbar
from tabulate import tabulate
from lingpy.compare.sanity import average_coverage
from collections import defaultdict

def run(args):

    ds = Dataset(args)
    wl = Wordlist.from_cldf(str(ds.cldf_specs().metadata_path))
    
    table = []
    for k, v in wl.coverage().items():
        table += [[k, v, round(v/wl.height, 2)]]
    print(tabulate(table, headers=['doculect', 'items', 'proportion'],
        tablefmt='pipe'))
    print(average_coverage(wl))
    
    profile = set()
    for idx, tokens in wl.iter_rows('tokens'):

        clss = tokens2class(tokens, 'cv')
        print(wl[idx, 'doculect'], tokens, clss)
        previous = ''
        for i, (cls, sound) in enumerate(zip(clss, tokens)):
            if previous in 'VC' and cls == 'T':
                profile.add((tokens[i-1]+sound, sound+'/'+tokens[i-1]))
            previous = cls
    for s, t in profile:
        print('{0}\t{1}'.format(s, t))
