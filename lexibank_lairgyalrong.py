import attr
from pathlib import Path

from pylexibank import Concept, Language, Lexeme
from pylexibank import Dataset as BaseDataset
from pylexibank.util import progressbar

from clldutils.misc import slug

from pyedictor import fetch
from lingpy import Wordlist, basictypes


@attr.s
class CustomConcept(Concept):
    Huang_1992_1820_ID = attr.ib(default=None)
    Number = attr.ib(default=None)
    Lexibank_Gloss = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    LookupName = attr.ib(default=None)
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
    writer_options = dict(keep_languages=False, keep_parameters=False)

    def cmd_download(self, _):
        data = fetch(
                "rgyalrong", base_url="https://lingulist.de/edev",
                columns=[
                    "DOCULECT",
                    "CONCEPT",
                    "VALUE",
                    "FORM",
                    "TOKENS",
                    "MORPHEMES",
                    "COGIDS",
                    "COGID",
                    "ALIGNMENT",
                    "BORROWING",
                    "ID_IN_SOURCE",
                    "NOTE"
                    ])
        with open(self.raw_dir / "wordlist.tsv", "w") as f:
            f.write(data)

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        wl = Wordlist(str(self.raw_dir / "wordlist.tsv"))
        # later add concept list here
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            for gloss in concept.attributes["lexibank_gloss"]:
                idx = concept.number+"_"+slug(concept.english)
                args.writer.add_concept(
                        ID=idx,
                        Name=concept.english,
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss,
                        Number=concept.number,
                        Lexibank_Gloss=concept.attributes["lexibank_gloss"],
                        Huang_1992_1820_ID=concept.attributes["huang_1992_1820"]
                        )
                concepts[gloss] = idx

        # add languages
        languages = args.writer.add_languages(lookup_factory="LookupName")
        sources = {l["LookupName"]: l["Sources"] for l in self.languages}

        # add word forms
        for idx in progressbar(wl, desc="cldfify"):
            if wl[idx, "tokens"]:
                # compare data
                if len("".join(wl[idx, "tokens"]).split("+")) != len(wl[idx, "cogids"]):
                    args.log.info("error in word form {0} / {1} / {2}".format(
                        idx,
                        wl[idx, "concept"],
                        wl[idx, "doculect"]))
                if wl[idx, "concept"] in concepts:
                    args.writer.add_form_with_segments(
                            Local_ID=wl[idx, "id_in_source"],
                            Language_ID=languages[wl[idx, "doculect"]],
                            Parameter_ID=concepts[wl[idx, "concept"]],
                            Value=wl[idx, "value"].strip() or wl[idx, "form"].strip() or "?",
                            Form=wl[idx, "form"].strip() or wl[idx, "value"].strip() or "?",
                            Segments=wl[idx, "tokens"],
                            Partial_Cognacy=str(basictypes.ints(wl[idx, "cogids"])),
                            Source=sources[wl[idx, "doculect"]]
                            )
