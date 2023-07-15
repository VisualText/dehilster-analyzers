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
articles;
  
// articleRecord := RECORD
//   STRING filename;
//   STRING text;
// END;

// articleRecord DataToText(textRecord L) := TRANSFORM
//   SELF.filename := L.filename; 
//   SELF.text := (STRING)L.blob;
// END;

// Result := PROJECT(textData,DataToText(LEFT));
// Result;