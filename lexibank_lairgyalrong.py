import attr
from pathlib import Path

from pylexibank import Concept, Language, Lexeme
from pylexibank import Dataset as BaseDataset
from pylexibank.util import progressbar, getEvoBibAsBibtex

from clldutils.misc import slug

import lingpy
from lingpy.sequence.sound_classes import syllabify
from pyedictor import fetch
from lingpy import Wordlist

@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)
    Coverage = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    SubGroup = attr.ib(default=None)
    Coverage = attr.ib(default=None)
    Sources = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Partial_Cognacy = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "lairgyalrong"
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    def cmd_download(self, args):
        data = fetch("rgyalrong", base_url="https://lingulist.de/edev")
        with open(self.raw_dir / "wordlist.tsv", "w") as f:
            f.write(data)

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        wl = Wordlist(str(self.raw_dir / "wordlist.tsv"))
        # later add concept list here
        concepts = {}
        for concept in self.concepts:
            for gloss in concept["LEXIBANK_GLOSS"].split(" // "):
                if gloss in wl.rows:
                    idx = concept["NUMBER"]+"_"+slug(concept["ENGLISH"])
                    args.writer.add_concept(
                            ID=idx,
                            Name=concept["ENGLISH"],
                            Concepticon_ID=concept["CONCEPTICON_ID"],
                            Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                            )
                    concepts[gloss] = idx
        # check if all concepts are covered
        rest = [c for c in wl.rows if c not in concepts]
        if rest:
            for c in rest:
                args.log.info("missing concept {0}".format(c))
        else:
            args.log.info("all concepts were added")

        # add languages
        args.writer.add_languages()
        sources = {l["ID"]: l["Sources"] for l in self.languages}

        # add word forms
        for idx in progressbar(wl, desc="cldfify"):
            if wl[idx, "tokens"]:
                # compare data
                if len("".join(wl[idx, "tokens"]).split("+")) != len(wl[idx,
                                                                        "cogids"]):
                    args.log.info("error in word form {0} / {1} / {2}".format(
                        idx,
                        wl[idx, "concept"],
                        wl[idx, "doculect"]))
                args.writer.add_form_with_segments(
                        Local_ID=wl[idx, "id_in_source"],
                        Language_ID=wl[idx, "doculect"],
                        Parameter_ID=concepts[wl[idx, "concept"]],
                        Value=wl[idx, "value"].strip() or wl[idx,
                            "form"].strip() or "?",
                        Form=wl[idx, "form"].strip() or wl[idx,
                            "value"].strip() or "?",
                        Segments=wl[idx, "tokens"],
                        Partial_Cognacy=str(wl[idx, "cogids"]),
                        Source=sources[wl[idx, "doculect"]]
                        )


                

