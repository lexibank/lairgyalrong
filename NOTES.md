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
