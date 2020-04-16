"""
Compute cognates.
"""

from lingpy import *
from lexibank_lairgyalrong import Dataset as Dataset1
from lexibank_sagartst import Dataset as Dataset2
from lingpy.compare.partial import Partial
from pylexibank import progressbar
from lexibase.lexibase import LexiBase

def run(args):

    ds1 = Dataset1(args)
    ds2 = Dataset2(args)
    wl1 = Wordlist.from_cldf(
            str(ds1.cldf_specs().metadata_path),
            columns = (
                'local_id',
                'language_id',
                'language_name',
                'concept_name',
                'parameter_id',
                'value',
                'form',
                'segments',
                ),
            namespace = (
                ('concept_name', 'concept'),
                ('parameter_id', 'concepticon_id'),
                ('language_id', 'doculect'),
                ('language_name', 'doculect_name'),
                ('segments', 'tokens'),
                ('language_glottocode', 'glottolog'),
                ('concept_concepticon_id', 'concepticon'),
                ('language_latitude', 'latitude'),
                ('language_longitude', 'longitude'),
                ('cognacy', 'cognacy'),
                ('local_id', 'id_in_source'),
                ('cogid_cognateset_id', 'cogid'))
            )
    args.log.info('loaded dataset 1')
    wl2 = Wordlist.from_cldf(
            str(ds2.cldf_specs().metadata_path),
            columns = (
                'local_id',
                'language_id',
                'language_name',
                'concept_name',
                'parameter_id',
                'value',
                'form',
                'segments',
                'cogid_cognateset_id'
                ),
            namespace = (
                ('concept_name', 'concept'),
                ('language_id', 'doculect'),
                ('segments', 'tokens'),
                ('language_glottocode', 'glottolog'),
                ('concept_concepticon_id', 'concepticon'),
                ('language_latitude', 'latitude'),
                ('language_longitude', 'longitude'),
                ('cognacy', 'cognacy'),
                ('local_id', 'id_in_source'),
                ('cogid_cognateset_id', 'cogid'))
            )
    args.log.info('loaded dataset 2')

    
    bylocal = {wl2[idx, 'id_in_source']: idx for idx in wl2}
    cognates = {}
    for idx, lid in progressbar(wl1.iter_rows('id_in_source'), desc='cognates'):
        if lid in bylocal:
            cognates[idx] = wl2[bylocal[lid], 'cogid']
        else:
            cognates[idx] = 0

    wl1.add_entries('cogid', cognates, lambda x: x)
    args.log.info('starting partial cognate detection')

    wl = {0: wl1.columns}
    for idx in wl1:
        wl[idx] = wl1[idx]

    part = Partial(wl)
    part.get_partial_scorer(runs=1000)
    part.partial_cluster(method='lexstat', threshold=0.45,
            cluster_method='infomap', ref='cogids')

    part.output(
            'tsv',
            filename=ds1.dir.joinpath(
                'analysis',
                'wordlist-cognates'
                ).as_posix(),
            ignore='all',
            prettify=False
            )



