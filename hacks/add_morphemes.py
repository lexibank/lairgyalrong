from lexibase import LexiBase
from lingpy import *
from collections import defaultdict
from clldutils.text import strip_brackets, split_text
from clldutils.misc import slug
from lingpy.convert.strings import write_nexus

# cogids2cogid
def cogids2cogid(wordlist, ref="cogids", cognates="cogid", morphemes="morphemes"):
    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(" ", "_")
        base = slug(base).upper()
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
        url='rgyalrong.sqlite3',
        )
D = {0: [h for h in lex.columns]}
lex.add_entries('sagartid', 'cogid', lambda x: x)
for idx in lex:
    try:
        lex[idx, 'cogids'] = basictypes.ints(cogids)
    except:
        pass
    if len(basictypes.lists(lex[idx, 'tokens']).n) != len(
            basictypes.strings(lex[idx, 'cogids'])):
        lex[idx, 'note'] = '!cognates'
    else:
        if not 'NaN' in lex[idx, 'cogids'] and lex[idx, 'cogids'].strip():
            D[idx] = [lex[idx, h] for h in D[0]]

wl = Wordlist(D)


cogids2cogid(wl, morphemes='glosses')

#lex.add_entries('morphemes', 'cogids', lambda x: '')
#for idx in wl:
#    lex[idx, 'morphemes'] = wl[idx, 'morphemes']
#    lex[idx, 'cogid'] = int(wl[idx, 'cogid'])
#
#lex.output('tsv', filename='rgyalrong-cogid', ignore='all')

new_idx = max([wl[idx, 'cogid'] for idx in wl])+1
for idx in wl:
    if wl[idx, 'borrowing'].strip():
        wl[idx, 'cogid'] = new_idx
        new_idx += 1
    elif '!' in wl[idx, 'note']:
        wl[idx, 'cogid'] = new_idx
        new_idx += 1
    try:
        wl[idx, 'cogid'] = int(wl[idx, 'cogid'])
    except:
        print('problem', idx, wl[idx, 'cogid'])

commands = [
    "set autoclose=yes nowarn=yes;",
    "lset coding=noabsencesites rates=gamma;",
    "taxset fossils = Tangut OldBurmese;",
    "constraint root = 1-.;",
    "calibrate OldBurmese = fixed(800);",
    "calibrate Tangut = fixed(900);",
    "prset clockratepr=exponential(3e5);",
    "prset treeagepr=uniform(3000,20000);",
    "prset sampleprob=0.2 samplestrat=random speciationpr=exp(1);",
    "prset extinctionpr=beta(1,1) nodeagepr=calibrated;prset brlenspr=clock:fossilization clockvarpr=igr;",
    "mcmcp ngen=10000000 printfreq=10000 samplefreq=2000 nruns=2 nchains=4 savebrlens=yes filename=rgyalrong-mrbayes-out;",
    ]

write_nexus(wl, ref='cogid', mode='mrbayes', filename='rgyalrong-mrbayes.nex',
        commands=commands)

wl.output('tsv', filename='rgyalrong-check')
