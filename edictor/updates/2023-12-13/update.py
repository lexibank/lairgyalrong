from pyedictor import fetch
from lexibase import LexiBase
import pathlib
from csvw.dsv import UnicodeDictReader
from lingpy import *
from tabulate import tabulate
from warnings import warn


path = pathlib.Path(__file__).parent.parent.parent.parent
raw_path = path / "raw"


new_word_lists = [
        "YaojiSitu", "CogtseSitu", "NjorogsKhroskyabs",
        "mBrongrdzongKhroskyabs", "BawangHorpa", "JRYYSitu", "ShimuliuJaphug",
        ]

languages = {}
with UnicodeDictReader(path / "etc" / "languages.csv") as reader:
    for row in reader:
        languages[row["LookupName"]] = row


lex = LexiBase(str(raw_path / "wordlist.tsv"))

for pth in new_word_lists:
    data = {0: lex.columns}
    idx = 1
    wl_path = raw_path / str(pth + ".tsv")
    if wl_path.exists():
        with UnicodeDictReader(raw_path / str(pth + ".tsv"), delimiter="\t") as reader:
            for row in reader:
                row["DOCULECT"] = pth
                if row["VALUE"].strip():
                    data[idx] = []
                    for h in data[0]:
                        data[idx] += [row.get(h.upper(), "")]
                    idx += 1
        wl = Wordlist(data)
        for idx, form in wl.iter_rows("value"):
            wl[idx, "form"] = form.replace(" ", "_")
            wl[idx, "tokens"] = ipa2tokens(form.replace(" ", "_"))
        lex.add_data(wl)
    else:
        warn(pth + ".tsv does not exist")

lex.add_entries(
        "subgroup", "doculect", 
        lambda x: languages[x]["SubGroup"])
for idx, doculect in lex.iter_rows("doculect"):
    lex[idx, "doculect"] = languages[doculect]["Name"]

lex.output('tsv', filename="new_data", ignore="all", prettify=False)
lex = LexiBase("new_data.tsv")
lex.db = "lairgyalrong.sqlite3"
table = [(k, v, v / lex.height) for k, v in lex.coverage().items()]
print(tabulate(table, tablefmt="pipe", headers=["Doculect", "Items", "Coverage"]))
lex.create("lairgyalrong")
