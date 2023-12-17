# wiktionary-java

An offline dictionary based on Wiktionary.<br/>

## Screenshots
![image](https://github.com/mustafa-mohamed-k/wiktionary-java/assets/66688103/0afe25a6-dcbf-440b-a559-5a694dc5607e)


## Building the database file
The database file is an SQLite file built by reading the .json file found at [Large JSON file with word senses - > 1GB](https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.json).<br/>
The database file is built using Python. To build the database, perform the following steps.<br/>
1. cd into the [python folder](python).<br/>
2. Ensure the .json file is in the [python folder](python) folder.<br/>
3. Ensure the `dictionary.sqlite` file is in the [python folder](python) folder.
 The commands to create the sqlite file can be found in [dictionary.sqlite.sql](python\dictionary.sqlite.sql).<br/>
4. Run `python -m venv venv` to create a virtual environment (on Windows).<br/>
5. Activate the virtual environment using `venv/Scripts/activate` (on Windows)<br/>
6. Install python packages using `pip install -r requirements.txt`<br/>
7. Run `python main.py`. Executing this command will clear the database and insert new records afresh. This takes a while, roughly 30 minutes depending on your computer.<br/>
8. It might be useful to run `VACUUM` on the database file in order to free up file space.<br/>

## License
Definitions fetched from wiktionary are licensed as described in [this page](https://en.wiktionary.org/wiki/Wiktionary:Copyrights).

## References
[wiktextract on pypi](https://pypi.org/project/wiktextract/)<br/>
[kaikki.org](https://kaikki.org)<br/>
[wiktextract on Github](https://github.com/tatuylonen/wiktextract)<br/>
[Large JSON file with word senses - > 1GB](https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.json)<br/>
