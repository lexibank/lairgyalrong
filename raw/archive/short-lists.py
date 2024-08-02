from lingpy import *

wl = Wordlist('rgyalrongic phylogeny.tsv')
wl.add_entries('sagart_id', 'concept', lambda x: '')
wl.add_entries('value', 'ipa', lambda x: x)
wl.add_entries('form', 'ipa', lambda x: x)
for idx in wl:
    wl[idx, 'sagart_id'] = idx
for lang in wl.cols:
    wl.output('tsv', filename=lang, ignore='all', subset=True, 
            rows=dict(
                doculect = '== "'+lang+'"'), prettify=False,
            cols=[
                'CONCEPT',
                'CHINESE',
                'GLOSS_IN_SOURCE',
                'VALUE',
                'FORM',
                'TOKENS',
                'MORPHEME_STRUCTURE',
                'BORROWING',
                'SAGART_ID',
                'NOTE',
                'COGID']
            )
    print(lang, len(wl.get_list(col=lang, flat=True)))
