# CLDF dataset derived from Lai and List's "Comparison of Rgyalrongic Languages" from 2023

[![CLDF validation](https://github.com/lexibank/lairgyalrong/workflows/CLDF-validation/badge.svg)](https://github.com/lexibank/lairgyalrong/actions?query=workflow%3ACLDF-validation)

## How to cite

If you use these data please cite
- the original source
  > Lai, Yunfan and List, Johann-Mattis (2023): Lexical Data for the Historical Comparison of Rgyalrongic Languages [Dataset, Version 1.0]. Leipzig: Max Planck Institute for Evolutionary Anthropology.
- the derived dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This dataset is licensed under a CC-BY-4.0 license

Available online at http://github.com/lexibank/lairgyalrong


Conceptlists in Concepticon:
- [Lai-2023-291](https://concepticon.clld.org/contributions/Lai-2023-291)
## Notes

In order to convert the data to the TSV format compatible with EDICTOR (and easy to browse in Excel), you can use `pyedictor`:

```
$ pip install pyedictor
$ edictor wordlist --name=lairgyalrong --addon="partial_cognacy:cogids"
```

This will output the data to the file `lairgyalrong.tsv`. For convenience, we allow users to access the file via EDICTOR directly, using the following link:

```
https://digling.org/edictor/?file=lairgyalrong.tsv&preview=500&basics=DOCULECT|CONCEPT|TOKENS|COGIDS&publish=true
```

With this link, you can browse the data in the EDICTOR tool online (without being able to manipulate the data).



## Statistics


[![CLDF validation](https://github.com/lexibank/lairgyalrong/workflows/CLDF-validation/badge.svg)](https://github.com/lexibank/lairgyalrong/actions?query=workflow%3ACLDF-validation)
![Glottolog: 100%](https://img.shields.io/badge/Glottolog-100%25-brightgreen.svg "Glottolog: 100%")
![Concepticon: 100%](https://img.shields.io/badge/Concepticon-100%25-brightgreen.svg "Concepticon: 100%")
![Source: 86%](https://img.shields.io/badge/Source-86%25-yellowgreen.svg "Source: 86%")
![BIPA: 100%](https://img.shields.io/badge/BIPA-100%25-brightgreen.svg "BIPA: 100%")
![CLTS SoundClass: 100%](https://img.shields.io/badge/CLTS%20SoundClass-100%25-brightgreen.svg "CLTS SoundClass: 100%")

- **Varieties:** 22 (linked to 18 different Glottocodes)
- **Concepts:** 291 (linked to 291 different Concepticon concept sets)
- **Lexemes:** 6,321
- **Sources:** 15
- **Synonymy:** 1.10
- **Invalid lexemes:** 0
- **Tokens:** 29,381
- **Segments:** 414 (0 BIPA errors, 0 CLTS sound class errors, 407 CLTS modified)
- **Inventory size (avg):** 72.32

## Possible Improvements:



- Entries missing sources: 895/6321 (14.16%)

# Contributors

Name | GitHub user | Description | Role
 --- | --- | --- | ----
Yunfan Lai | |  | Author
Johann-Mattis List | @lingulist | maintainer | Author, Editor




## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [Wordlist](https://github.com/cldf/cldf/tree/master/modules/Wordlist) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)