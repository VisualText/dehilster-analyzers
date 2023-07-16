nlp := SERVICE : plugin('nlp'), namespace('nlp'), library('nlp'), CPP, PURE
  string AnalyzeText(const string analyzer, const string txt) : cpp,pure,context,entrypoint='AnalyzeText';
  unicode UnicodeAnalyzeText(const string analyzer, const unicode txt) : cpp,pure,context,entrypoint='AnalyzeTextU';
END;

article := RECORD
  STRING title;
  STRING url;
  STRING text;
END;
articles := DATASET('~doj::articles::dojarticles.xml',article,XML('articles/article'));

nlpResults := RECORD
  STRING title;
  INTEGER id;
  STRING url;
  STRING xmlEntities;
END;
  
nlpResults ExtractEntities(article L, INTEGER c) := TRANSFORM
  SELF.title := L.title;
  SELF.id := c;
  SELF.url := L.url;
  SELF.xmlEntities := nlp.AnalyzeText('Entities',L.text);
END;

entities := PROJECT(articles,ExtractEntities(LEFT,COUNTER));
entities;

personRec := RECORD
  INTEGER articleID;
  STRING name;
  STRING title;
  STRING age;
  STRING city;
  STRING state;
  STRING country;
END;

personRec extractPerson(nlpResults L) := TRANSFORM
  SELF.articleID := L.id;
  SELF.name := XMLTEXT('name');
  SELF.title := XMLTEXT('title');
  SELF.age := XMLTEXT('age');
  SELF.city := XMLTEXT('city');
  SELF.state := XMLTEXT('state');
  SELF.country := XMLTEXT('country');
END;

out := PARSE(entities, xmlEntities, extractPerson(LEFT), XML('people/person'));
OUTPUT(out);


