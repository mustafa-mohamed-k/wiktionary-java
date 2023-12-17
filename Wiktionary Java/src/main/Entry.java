package main;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Mustafa Mohamed
 */
public class Entry {

    public int id;
    public String word;
    public String pos;
    public String lang;
    public String langCode;
    public String etymologyText;

    public List<Sense> senses = new ArrayList<>();
    public List<Antonym> antonyms = new ArrayList<>();
    public List<CoordianteTerm> coordianteTerms = new ArrayList<>();
    public List<Derived> deriveds = new ArrayList<>();
    public List<DerivedWord> derivedWords = new ArrayList<>();
    public List<Holonym> holonyms = new ArrayList<>();
    public List<Hypernym> hypernyms = new ArrayList<>();
    public List<Meronym> meronyms = new ArrayList<>();
    public List<Related> relateds = new ArrayList<>();
    public List<Sound> sounds = new ArrayList<>();
    public List<Synonym> synonyms = new ArrayList<>();
}
