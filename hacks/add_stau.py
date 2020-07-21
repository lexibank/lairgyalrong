from lexibase import LexiBase
from lingpy import *

lex = LexiBase.from_dbase(
        table='rgyalrong',
        dbase='rgyalrong.sqlite3',
        url='rgyalrong.sqlite3',
        )

stau = csv2list('../raw/MazurStau.tsv', strip_lines=False)
S = {0: ['DOCULECT']+[h for h in stau[0][1:]]}
for i, line in enumerate(stau[1:]):
    tmp = dict(zip(stau[0], line))
    tmp['TOKENS'] = ipa2tokens(tmp['FORM'])
    tmp['DOCULECT'] = 'MazurStau'
    row = []
    for h in S[0]:
        row += [tmp[h]]
    S[i+1] = row
wl = Wordlist(S)
lex.add_data(wl)
lex.vacuum()
lex.update()

