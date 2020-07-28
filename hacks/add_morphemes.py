from lexibase import LexiBase
from lingpy import *
from collections import defaultdict
from clldutils.text import strip_brackets, split_text
from lingpy.convert.strings import write_nexus

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
        if not 'NaN' in lex[idx, 'cogids'] and lex[idx, 'cogids'].strip():
            D[idx] = [lex[idx, h] for h in D[0]]

wl = Wordlist(D)


cogids2cogid(wl)

lex.add_entries('morphemes', 'cogids', lambda x: '')
for idx in wl:
    lex[idx, 'morphemes'] = wl[idx, 'morphemes']
    lex[idx, 'cogid'] = int(wl[idx, 'cogid'])

lex.output('tsv', filename='rgyalrong-cogid', ignore='all')

new_idx = max([wl[idx, 'cogid'] for idx in wl])+1
for idx in lex:
    if lex[idx, 'borrowing'].strip():
        lex[idx, 'cogid'] = new_idx
        new_idx += 1
    elif '!' in lex[idx, 'note']:
        lex[idx, 'cogid'] = new_idx
        new_idx += 1
    try:
        lex[idx, 'cogid'] = int(lex[idx, 'cogid'])
    except:
        print('problem', idx, lex[idx, 'cogid'])

write_nexus(wl, ref='cogid', mode='splitstree', filename='rgyalrong-st.nex')
