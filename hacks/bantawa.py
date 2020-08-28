from lexibase.lexibase import LexiBase
from lingpy import *
from lingpy.compare.partial import Partial

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
        #url='rgyalrong.sqlite3',
        )

D = {0: lex.columns}
for idx in lex:
    lex[idx, 'tokens'] = basictypes.lists(lex[idx, 'tokens'])
    try:
        lex[idx, 'cogids'] = basictypes.ints(lex[idx, 'cogids'])
    except:
        print(idx, lex[idx, 'doculect'], lex[idx, 'concept'], lex[idx,
            'cogids'])

    D[idx] = lex[idx]
    

for idx in lex:
    try:
        tokens2class(lex[idx, 'tokens'], 'sca')
    except:
        print(idx, lex[idx, 'doculect'], lex[idx, 'concept'], lex[idx,
            'tokens'])


part = Partial(D)
part.get_partial_scorer()
part.partial_cluster(method='lexstat', threshold=0.55, ref='lexstatids')
part.partial_cluster(method='sca', threshold=0.55, ref='scaids')


etd = part.get_etymdict(ref='scaids')
count = 1
outf = open('sca-cognates.tsv', 'w')
for cogid in etd:
    idxs = []
    for idx in etd[cogid]:
        if idx:
            idxs += idx
    docs = [part[idx, 'doculect'] for idx in idxs]
    if 'Bantawa' in docs and len(set(docs)) > 1:
        print(count, '\t', part[idxs[0], 'concept'], '\t', part[idxs[0],
            'tokens'], len(set(docs)))
        outf.write('\t'.join(
            [str(count), part[idxs[0], 'concept'], str(part[idxs[0], 'tokens']),
                str(len(set(docs)))])+'\n')
        count += 1
outf.close()

etd = part.get_etymdict(ref='lexstatids')
count = 1
outf = open('lexstat-cognates.tsv', 'w')
for cogid in etd:
    idxs = []
    for idx in etd[cogid]:
        if idx:
            idxs += idx
    docs = [part[idx, 'doculect'] for idx in idxs]
    if 'Bantawa' in docs and len(set(docs)) > 1:
        print(count, '\t', part[idxs[0], 'concept'], '\t', str(part[idxs[0],
            'tokens']), len(set(docs)))
        outf.write('\t'.join(
            [str(count), part[idxs[0], 'concept'], str(part[idxs[0], 'tokens']),
                str(len(set(docs)))])+'\n')
        count += 1
outf.close()

part.output('tsv', filename='automated-cognates', ignore='all', prettify=False)
