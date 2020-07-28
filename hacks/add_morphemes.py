from lexibase import LexiBase
from lingpy import *
from collections import defaultdict
from clldutils.text import strip_brackets, split_text

# cogids2cogid
def cogids2cogid(wordlist, ref="cogids", cognates="cogid", morphemes="morphemes"):
    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(" ", "_")
        idxs = wordlist.get_list(row=concept, flat=True)
        cogids = defaultdict(list)
        for idx in idxs:
            M[idx] = [c for c in basictypes.ints(wordlist[idx, ref])]
            for cogid in basictypes.ints(wordlist[idx, ref]):
                cogids[cogid] += [idx]
        
        for i, (cogid, idxs) in enumerate(
            sorted(cogids.items(), key=lambda x: len(x[1]), reverse=True)
        ):
            print(cogid, idxs)
            for idx in idxs:
                if idx not in C:
                    print(M[idx])
                    C[idx] = current
                    M[idx][M[idx].index(cogid)] = base
                else:
                    M[idx][M[idx].index(cogid)] = "_" + base.lower()
            current += 1
    wordlist.add_entries(cognates, C, lambda x: x)
    if morphemes:
        wordlist.add_entries(morphemes, M, lambda x: x)

lex = LexiBase.from_dbase(
        table='rgyalrong',
        dbase='rgyalrong.sqlite3',
        #url='rgyalrong.sqlite3',
        )
D = {0: [h for h in lex.columns]}
lex.add_entries('sagartid', 'cogid', lambda x: x)
for idx in lex:
    try:
        lex[idx, 'cogids'] = basictypes.intes(cogids)
    except:
        pass
    if len(basictypes.lists(lex[idx, 'tokens']).n) != len(
            basictypes.strings(lex[idx, 'cogids'])):
        lex[idx, 'note'] = '!cognates'
    else:
        if not 'NaN' in lex[idx, 'cogids']:
            D[idx] = [lex[idx, h] for h in D[0]]

wl = Wordlist(D)


cogids2cogid(wl)

lex.add_entries('morphemes', 'cogids', lambda x: '')
for idx in wl:
    lex[idx, 'morphemes'] = wl[idx, 'morphemes']
    lex[idx, 'cogid'] = wl[idx, 'cogid']

lex.output('tsv', filename='rgyalrong-cogid', ignore='all')
