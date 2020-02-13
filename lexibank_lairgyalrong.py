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


@attr.s
class CustomLanguage(Language):
    ChineseName = attr.ib(default=None)
    #SubGroup = attr.ib(default="Sinitic")
    Family = attr.ib(default="Sino-Tibetan")
    DialectGroup = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Benzi = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "lairgyalrong"
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        concepts = args.writer.add_concepts(
                id_factory=lambda x: '{0}_{1}'.format(x.number,
                    slug(x.english)),
                lookup_factory='Name')
        print(concepts)
        missing = set()
        
        for wlfile in self.raw_dir.glob('*.tsv'):
            language = wlfile.name[:-4]
            args.log.info("parsing {0}".format(language))
            try:
                wl = lingpy.Wordlist(wlfile.as_posix())
            except:
                D = {0: ['doculect', 'concept', 'value', 'form']}
                for i, row in enumerate(self.raw_dir.read_csv(
                        wlfile, delimiter='\t', dicts=True)):
                    D[i+1] = [language, row['CONCEPT'], row['FORM'], row['VALUE']]
                wl = lingpy.Wordlist(D)

            args.writer.add_language(
                    ID=language,
                    Name=language)
            for idx in wl:
                if wl[idx, 'concept'] in concepts and (
                        wl[idx, 'value'].strip() or wl[idx, 'form'].strip()):
                    args.writer.add_form(
                            Parameter_ID=concepts[wl[idx, 'concept']],
                            Language_ID=language,
                            Value=wl[idx, 'value'].strip() or wl[idx, 'form'],
                            Form=wl[idx, 'form'].strip() or wl[idx, 'value']
                            )
                else:
                    args.log.info('Missing concept {0}'.format(wl[idx,
                        'concept']))
                    missing.add(wl[idx, 'concept'])
        for m in sorted(missing):
            print(m)
        input()
                

