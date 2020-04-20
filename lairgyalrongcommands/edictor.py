"""
Convert data to edictor application.
"""

from lingpy import *
from lexibank_lairgyalrong import Dataset
from lexibank_sagartst import Dataset as Dataset2
from lingpy.compare.partial import Partial
from pylexibank import progressbar
from lexibase.lexibase import LexiBase

def run(args):

    ds = Dataset(args)
    alms = Alignments(
            ds.dir.joinpath('analysis', 'wordlist-cognates.tsv').as_posix(),
            ref='cogids')
    alms.align()
    alms.add_entries('note', 'value', lambda x: '')
    alms.add_entries('borrowing', 'value', lambda x: '')
    D = {0: [
        'id_in_source',
        'doculect',
        'concept',
        'value',
        'form',
        'tokens',
        'cogid',
        'cogids',
        'alignment',
        'borrowing',
        'note'
        ]}
    for idx in alms:
        D[idx] = [alms[idx, h] for h in D[0]]
    lex = LexiBase(
            D, 
            dbase=ds.dir.joinpath(
                'analysis',
                'rgyalrong.sqlite3').as_posix()
            )
    lex.create(table='rgyalrong')




