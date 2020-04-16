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
    lex = LexiBase(
            alms, 
            dbase=ds.dir.joinpath(
                'analysis',
                'rgyalrong.sqlite3').as_posix()
            )
    lex.create(table='rgyalrong')




