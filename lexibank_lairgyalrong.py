import attr
from pathlib import Path

from pylexibank import Concept, Language, Lexeme
from pylexibank import Dataset as BaseDataset
from pylexibank.util import progressbar, getEvoBibAsBibtex

from clldutils.misc import slug

import lingpy
from lingpy.sequence.sound_classes import syllabify


@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)
    Coverage = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")
    DialectGroup = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Benzi = attr.ib(default=None)
    Sagart_ID = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "lairgyalrong"
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        concept_coverage = {c['ENGLISH']: 0 for c in self.concepts}
        D = {0: ['doculect', 'concept', 'value', 'form', 'source', 'sagart_id']}
        gidx = 1
        for language in self.languages:
            args.log.info("parsing {0}".format(language['Name']))
            for row in self.raw_dir.read_csv(
                language['ID']+'.tsv', delimiter='\t', dicts=True):
                if row['CONCEPT'] not in ['UNKNOWN', 'GLOSS', '']:
                    D[gidx] = [
                        language['ID'], 
                        row['CONCEPT'], 
                        row['FORM'], 
                        row['VALUE'],
                        language['Source'],
                        row['ID']
                        ]
                    concept_coverage[row['CONCEPT']] += 1
                    gidx += 1
            
            args.writer.add_language(
                    ID=language['ID'],
                    Name=language['Name'],
                    Glottocode=language['Glottocode'],
                    Latitude=language['Latitude'],
                    Longitude=language['Longitude'],
                    SubGroup=language['SubGroup']
                    )
        wl = lingpy.Wordlist(D)
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(
                    concept['NUMBER'],
                    slug(concept['ENGLISH'])
                    )
            args.writer.add_concept(
                ID=idx,
                Name=concept['ENGLISH'],
                Concepticon_ID=concept['CONCEPTICON_ID'],
                Concepticon_Gloss=concept['CONCEPTICON_GLOSS'],
                Coverage=concept_coverage[concept["ENGLISH"]]
                )
            concepts[concept['ENGLISH']] = idx
            args.log.info('added concept {0}'.format(concept['ENGLISH']))
        for idx, language, concept, value, form, source, sid in wl.iter_rows('doculect', 
                'concept', 'value', 'form', 'source', 'sagart_id'):
            args.writer.add_form(
                    Language_ID=language,
                    Parameter_ID=concepts[concept],
                    Value=value if value else form,
                    Form=form if form else value,
                    Source=[source],
                    Sagart_ID=sid
                    )

        wl.output('tsv',
                filename=self.raw_dir.joinpath('rgyalrong').as_posix(),
                ignore='all', prettify=False)



                

