package main;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Mustafa Mohamed
 */
public class Sense {

    public int id;
    public String english;
    public int entryId;

    public List<AltOf> altOfs = new ArrayList<>();
    public List<Antonym> antonyms = new ArrayList<>();
    public List<Category> categories = new ArrayList<>();
    public List<CoordianteTerm> coordianteTerms = new ArrayList<>();
    public List<Derived> deriveds = new ArrayList<>();
    public List<DerivedWord> derivedWords = new ArrayList<>();
    public List<Example> examples = new ArrayList<>();
    public List<FormOf> formOfs = new ArrayList<>();
    public List<Gloss> glosses = new ArrayList<>();
    public List<Holonym> holonyms = new ArrayList<>();
    public List<Hypernym> hypernyms = new ArrayList<>();
    public List<Meronym> meronyms = new ArrayList<>();
    public List<RawGloss> rawGlosses = new ArrayList<>();
    public List<Related> relateds = new ArrayList<>();
    public List<Synonym> synonyms = new ArrayList<>();
    public List<Tag> tags = new ArrayList<>();
    public List<Topic> topics = new ArrayList<>();
    
}
