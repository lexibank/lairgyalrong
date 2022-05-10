"""
List aspects of the data.
"""

from lexibank_lairgyalrong import Dataset as LG
from pycldf import Dataset
from cltoolkit import Wordlist
from cldfbench.cli_util import add_catalog_spec
from clldutils.clilib import Table, add_format


def register(parser):
    add_catalog_spec(parser, "clts")
    add_catalog_spec(parser, "concepticon")
    add_format(parser, default="simple")
    parser.add_argument("--languages", action="store_true", help="plot languages")


def run(args):
    
    wls = Wordlist(
            [Dataset.from_metadata(
                LG().cldf_dir.joinpath(
                    "cldf-metadata.json"))], 
            ts=args.clts.api.bipa
            )
    if args.languages:
        with Table(args, "Name", "Subgroup", "Concepts", "Forms", "Coverage") as table:
            for language in wls.languages:
                table.append([
                    language.name,
                    language.data["SubGroup"],
                    len(language.concepts),
                    len(language.forms),
                    len(language.concepts) / len(wls.concepts),
                    ])


