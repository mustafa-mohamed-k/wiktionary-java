import json
from traceback import print_exc
from typing import Dict, List
from alive_progress import alive_bar

from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///dictionary.sqlite")


def add_x_nym(conn, table_name, key_name, sense, sense_id):
    if values := sense.get(key_name):
        for value in values:
            sql = (f"INSERT INTO {table_name} (alt, english, roman, sense, tags, taxonomic, topics, word, entry_id, sense_id)"
                " VALUES(:alt, :english, :roman, :sense, :tags, :taxonomic, :topics, :word, :entry_id, :sense_id)")
            keys = ["alt", "english", "roman",
                    "sense", "word", "taxonomic"]
            params = {}
            params["tags"] = ", ".join(tags) if (tags := value.get("tags")) else None
            params["topics"] = ", ".join(topics) if (topics := value.get("topics")) else None
            for key in keys:
                params[key] = value.get(key)
            params["entry_id"] = None
            params["sense_id"] = sense_id
            conn.execute(text(sql), params)


def add_examples(conn, sense, sense_id):
    if examples := sense.get("examples"):
        for example in examples:
            sql = ("INSERT INTO example (sense_id, `text`, `ref`, english, `type`, roman, note)"
                   " VALUES(:sense_id, :text, :ref, :english, :type, :roman, :note)")
            keys = ["text", "ref", "english", "type", "roman", "note"]
            params = {}
            for key in keys:
                params[key] = example.get(key)
            params["sense_id"] = sense_id
            conn.execute(text(sql), params)


def add_sound(conn, entry, entry_id):
    if sounds := entry.get("sounds"):
        for sound in sounds:
            sql = ("INSERT INTO sound (entry_id, ipa, enpr, audio, ogg_url, mp3_url, `audio-ipa`, homophones, hyphenation, tags, `text`)"
                   " VALUES(:entry_id, :ipa, :enpr, :audio, :ogg_url, :mp3_url, :audio_ipa, :homophones, :hyphenation, :tags, :text)")
            keys = ["ipa", "enpr", "audio", "ogg_url", "mp3_url",
                    "homophones", "hyphenation", "text"]
            params = {}
            params["tags"] = ", ".join(sound.get("tags")) if sound.get("tags") else None
            for key in keys:
                params[key] = sound.get(key)
            params["audio_ipa"] = sound.get("audio-ipa")
            params["entry_id"] = entry_id
            conn.execute(text(sql), params)


try:
    with open("kaikki.org-dictionary-English.json", "r", encoding='utf-8') as file:
        print('.json file opened for reading')
        with engine.connect() as conn:
            print('Established connection to database')
            print('Clearing database')
            sql = "DELETE FROM `entry`"
            conn.execute(text(sql))
            print('Cleared database')
            print('Reading .json file')

            print('')

            line_number = 1
            num_rows = 1261507 # this numbe was determined manually. It is the number of lines in the .json file
            with alive_bar(num_rows, title="Processing words") as bar:
                while (line := file.readline()):
                    # print(f'Line number {line_number}: \x1b[K', end='')
                    line_number += 1
                    entry: Dict = json.loads(line)

                    bar.text = entry.get("word") or ""

                    # print("creating entry\x1b[K", end='')
                    sql = "INSERT INTO `entry` (`word`, pos, lang, lang_code, wikidata, etymology_text) VALUES(:word, :pos, :lang, :lang_code, :wikidata, :etymology_text)"
                    result = conn.execute(text(sql), {
                        "word": entry.get("word"),
                        "pos": entry.get("pos"),
                        "lang": entry.get("lang"),
                        "lang_code": entry.get("lang_code"),
                        "wikidata": str(entry.get("wikidata")),
                        "etymology_text": entry.get("etymology_text")
                    })
                    entry_id = result.lastrowid
                    if entry.get("senses"):
                        senses: List[Dict] = entry.get("senses")
                        # print(", creating word senses\x1b[K", end='')
                        sense_number = 0
                        for sense in senses:
                            # if sense_number > 0:
                            #     print('\x1B[6D\x1b[K', end='')
                            # print(f' {sense_number:<5}', end='')
                            sense_number += 1
                            sql = "INSERT INTO sense (english, entry_id) VALUES(:english, :entry_id)"
                            result = conn.execute(text(sql), {
                                "english": sense.get("english"),
                                "entry_id": entry_id
                            })
                            sense_id = result.lastrowid

                            # print(", adding glosess\x1b[K", end='')
                            if glosses := sense.get("glosses"):
                                for gloss in glosses:
                                    sql = "INSERT INTO gloss (sense_id, gloss) VALUES(:sense_id, :gloss)"
                                    conn.execute(
                                        text(sql), {"sense_id": sense_id, "gloss": gloss})

                            # print(", adding raw glosses\x1b[K", end='')
                            if sense.get("raw_glosses"):
                                raw_glosses: List[str] = sense.get("raw_glosses")
                                for raw_gloss in raw_glosses:
                                    sql = "INSERT INTO raw_gloss(sense_id, raw_gloss) VALUES(:sense_id, :raw_gloss)"
                                    conn.execute(
                                        text(sql), {"sense_id": sense_id, "raw_gloss": raw_gloss})

                            # print(", adding tags\x1b[K", end='')
                            if (tags := sense.get("tags")):
                                for tag in tags:
                                    sql = "INSERT INTO tag (sense_id, tag) VALUES(:sense_id, :tag)"
                                    conn.execute(
                                        text(sql), {"sense_id": sense_id, "tag": tag})

                            # print(", adding categories\x1b[K", end='')
                            if (categories := sense.get("categories")):
                                for category in categories:
                                    sql = ("INSERT INTO category (sense_id, name, kind, parents, source, orig, langcode)"
                                        " VALUES(:sense_id, :name, :kind, :parents, :source, :orig, :langcode)")
                                    params = {}
                                    for key in ["name", "kind", "source", "orig", "langcode"]:
                                        params[key] = category.get(key)
                                    params["parents"] = ",".join(
                                        category.get("parents"))
                                    params["sense_id"] = sense_id
                                    conn.execute(text(sql), params)

                            # print(", adding topics\x1b[K", end='')
                            if (topics := sense.get("topics")):
                                for topic in topics:
                                    sql = "INSERT INTO topic (sense_id, topic) VALUES(:sense_id, :topic)"
                                    conn.execute(
                                        text(sql), {"sense_id": sense_id, "topic": topic})

                            if (alt_ofs := sense.get("alt_of")):
                                for alt in alt_ofs:
                                    sql = "INSERT INTO alt_of (sense_id, word, extra) VALUES(:sense_id, :word, :extra)"
                                    conn.execute(text(sql), {"sense_id": sense_id, "word": alt.get(
                                        "word"), "extra": alt.get("extra")})

                            if (form_ofs := sense.get("form_of")):
                                for form in form_ofs:
                                    sql = "INSERT INTO form_of (sense_id, word, extra) VALUES(:sense_id, :word, :extra)"
                                    conn.execute(text(sql), {"sense_id": sense_id, "word": form.get(
                                        "word"), "extra": form.get("extra")})

                            # print(", adding synonyms, antonyms, hypernyms, etc.\x1b[K", end='')
                            add_x_nym(conn, "synonym", "synonyms", sense, sense_id)
                            add_x_nym(conn, "antonym", "antonyms", sense, sense_id)
                            add_x_nym(conn, "hypernym",
                                    "hypernyms", sense, sense_id)
                            add_x_nym(conn, "holonym", "holonyms", sense, sense_id)
                            add_x_nym(conn, "meronym", "meronyms", sense, sense_id)
                            add_x_nym(conn, "coordianate_term",
                                    "coordianate_terms", sense, sense_id)
                            add_x_nym(conn, "derived", "derived", sense, sense_id)
                            add_x_nym(conn, "related", "related", sense, sense_id)

                            # print(", adding examples\x1b[K", end='')
                            add_examples(conn, sense, sense_id)
                            # print(', adding sounds\x1b[K', end='')
                            add_sound(conn, entry, entry_id)

                    bar()

                    # print('', end='\r')

            print('')
            print('Done reading file')

            conn.commit()


except:
    print_exc()
