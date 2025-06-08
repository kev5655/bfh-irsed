# Information Retrieval and Search Engine Design (BTI2026) 25

## Beschreibung der Quelldaten

Die Quelldaten bestehen aus einer JSON-Datei (`prog_lang.json`), die strukturierte Informationen zu verschiedenen Programmiersprachen enthält. Für jede Sprache werden unter anderem folgende Aspekte dokumentiert: Geschichte, Paradigmen, Syntax, Versionen, Merkmale, Beispiele, Einfluss und Veröffentlichungsdaten. Die Daten stammen aus Wikipedia und enthalten sowohl technische Details als auch historische Hintergründe zu den jeweiligen Programmiersprachen.

### Enthaltene Programmiersprachen

Im Datensatz sind unter anderem folgende Programmiersprachen enthalten:

- [Elixir](https://en.wikipedia.org/wiki/Elixir_(programming_language))
- [MATLAB](https://en.wikipedia.org/wiki/MATLAB)
- [Rust](https://en.wikipedia.org/wiki/Rust_(programming_language))
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
- [R](https://en.wikipedia.org/wiki/R_(programming_language))
- [Zig](https://en.wikipedia.org/wiki/Zig_(programming_language))
- [Scala](https://en.wikipedia.org/wiki/Scala_(programming_language))
- [Haskell](https://en.wikipedia.org/wiki/Haskell)
- [PowerShell](https://en.wikipedia.org/wiki/PowerShell)
- [Java](https://en.wikipedia.org/wiki/Java_(programming_language))
- [Assembly Language](https://en.wikipedia.org/wiki/Assembly_language)
- [Swift](https://en.wikipedia.org/wiki/Swift_(programming_language))
- [Lua](https://en.wikipedia.org/wiki/Lua)
- [C#](https://en.wikipedia.org/wiki/C_Sharp_(programming_language))
- [C](https://en.wikipedia.org/wiki/C_(programming_language))
- [Ruby](https://en.wikipedia.org/wiki/Ruby_(programming_language))
- [Typescirpt](https://en.wikipedia.org/wiki/TypeScript)
- [Apache Groovy](https://en.wikipedia.org/wiki/Apache_Groovy)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Dart](https://en.wikipedia.org/wiki/Dart_(programming_language))
- [Go](https://en.wikipedia.org/wiki/Go_(programming_language))
- [Kotlin](https://en.wikipedia.org/wiki/Kotlin_(programming_language))
- [PHP](https://en.wikipedia.org/wiki/PHP)
- [C++](https://en.wikipedia.org/wiki/C%2B%2B)

Alle mögliche Sprachen die man verwenden könnte: [Programmiersprachen](https://en.wikipedia.org/wiki/List_of_programming_languages)


## Scraping

Im folgenden Abschnitt wird beschrieben, wie die Quelldaten mithilfe von Web-Scraping gewonnen wurden. Das zugehörige Jupyter-Notebook (`./scraper.ipynb`) enthält den vollständigen Ablauf und die Dokumentation des Scraping-Prozesses. Dort wird erläutert, welche Werkzeuge und Bibliotheken verwendet wurden, wie die Daten extrahiert und verarbeitet wurden und welche Herausforderungen dabei aufgetreten sind.

## Goldstandard

Der Goldstandard ist im ersten Block von (`./f1-calc.ipynb`) definiert. Weiterhin ist eine Excel-Datei im Projekt enthalten, die nicht alle Suchanfragen, aber die aktuellen Scores enthält.

## GUI

Das GUI ist im Ordner (`./gui/`) implementiert.

## Search-Engine Improvement

### Python-Versionierungsproblem

Habe ich bereits im Video besprochen.

Abfragen: `title:python`, `title:python3`, `title:python3.12`

### Go-Abfragen

Mit einer Synonymliste konnte dieses Problem gelöst werden, ist ebenfalls im Video besprochen.

Abfragen: `title:go`, `title:golang`

### Funktionale Programmiersprachen

Der F1-Score konnte für alle drei Abfragen erhöht werden. Grund dafür ist folgender Filter:

```xml
<filter class="solr.EnglishMinimalStemFilterFactory"/>
```

### Objektorientierte Programmiersprachen

Der F1-Score hat sich nur bei folgender Abfrage erhöht: `document:"object-oriented" AND NOT document:"functional"`

Abfragen: `document:object-oriented`, `document:"object-oriented" AND NOT document:"functional"`, `document:imperative`

Für weitere Informationen siehe `./f1-score.ipynb` oder `./GoldStandart.xlsx`.

### C#, C++ und C

Verbesserungen habe ich im Video besprochen.

Abfragen: `title:C#`, `C Sharp`, `C++`

### Übrige Abfragen

Die restlichen Abfragen konnten wenig bis gar nicht optimiert werden. Der Fokus lag nicht auf diesen, da sie eher Suchanfragen sind, die auch Kontextwissen benötigen.

## Ranking

Die Ranking-Evaluation wurde im Video besprochen und ist in folgenden zwei Dateien zu finden:

- `./ranking-functional.ipynb`
- `./ranking-object.ipynb`

## Metadaten

Die Metadaten wurden nachträglich gescraped und stammen ebenfalls von den Wikipedia-Einträgen der Programmiersprachen. Verwendet wurde die Tabelle auf der rechten Seite (wurde im Video erklärt).

Das Skript für das Scrapen der Metadaten und die Auswertung ist hier zu finden: `./scraper_meta.ipynb`

### Analyse der Metadaten und Keys

Um einen besseren Überblick über die Daten zu erhalten, habe ich ein Skript geschrieben, das verschiedene Diagramme erstellt – zum Beispiel wie oft ein Key vorkommt oder welche Wörter wie oft unter welchem Key existieren – um Suchanfragen zu verbessern.

## Facet

Ein Skript, um mit Facetten zu experimentieren, liegt hier: `./facet.ipynb`

## Knowledge Graph

Der Knowledge Graph wurde mithilfe des Metadatenfeldes `influenced_by` erstellt.
Es wurde eine Facetten-Suchanfrage erstellt, so konnten wir die Daten evaluieren.

Das Skript ist hier zu finden: `./semantic-knowledge-graph.ipynb`

Das generierte Diagramm ist hier: `./programming_languages_influence.html`

## Gui

Die grafische Benutzeroberfläche (GUI) ermöglicht es, gezielt nach Programmiersprachen zu suchen und die Ergebnisse übersichtlich darzustellen. Nutzer können nach Namen, Paradigmen, Typisierung, Jahr und weiteren Eigenschaften filtern. Die Suchergebnisse werden als Liste angezeigt und können im Detail betrachtet werden. Das GUI ist für eine einfache und intuitive Bedienung ausgelegt und erleichtert den Zugriff auf die gesammelten und strukturierten Programmiersprachen-Daten.

## Final Solar `schema.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>

<schema name="default-config" version="1.6">
  <uniqueKey>url</uniqueKey>

  <fieldType name="title_en" class="solr.TextField" positionIncrementGap="100">

    <!-- this one is for indexing -->
    <analyzer type="index">
      <!-- strip #, ++ -->
      <charFilter class="solr.PatternReplaceCharFilterFactory"
                  pattern="(?&lt;=[Cc])#"
                  replacement=" sharp"/>
      <charFilter class="solr.PatternReplaceCharFilterFactory"
                  pattern="\+\+"
                  replacement=" plus plus"/>

      <tokenizer class="solr.StandardTokenizerFactory"/>
      <filter class="solr.LowerCaseFilterFactory"/>
      <filter class="solr.WordDelimiterGraphFilterFactory"/>
      <filter class="solr.FlattenGraphFilterFactory"/>
      <filter class="solr.SnowballPorterFilterFactory"/>
    </analyzer>

    <analyzer type="query">
      <!-- strip #, ++ -->
      <charFilter class="solr.PatternReplaceCharFilterFactory"
                  pattern="(?&lt;=[Cc])#"
                  replacement=" sharp"/>
      <charFilter class="solr.PatternReplaceCharFilterFactory"
                  pattern="\+\+"
                  replacement=" plus plus"/>

      <tokenizer class="solr.StandardTokenizerFactory"/>
      <filter class="solr.LowerCaseFilterFactory"/>
      <filter class="solr.WordDelimiterGraphFilterFactory"/>
            <filter class="solr.SynonymGraphFilterFactory"
              expand="true"
              ignoreCase="true"
              synonyms="synonyms_prog_en.txt"/>
      <filter class="solr.SnowballPorterFilterFactory"/>
    </analyzer>

  </fieldType>

  <fieldType name="text_en_prog" class="solr.TextField" positionIncrementGap="100">
    <analyzer>
      <tokenizer class="solr.StandardTokenizerFactory"/>
      <filter class="solr.LowerCaseFilterFactory"/>
      <filter class="solr.SynonymGraphFilterFactory"
              expand="true"
              ignoreCase="true"
              synonyms="synonyms_prog_en.txt"/>
      <filter class="solr.StopFilterFactory"
              words="stopwords_prog_en.txt"
              ignoreCase="true"/>
      <!-- Leichter englischer Stemmer (kein Porter, um Fachbegriffe zu schonen) -->
      <filter class="solr.EnglishMinimalStemFilterFactory"/>
      <!-- ASCII-Folding, damit “résumé” ≙ “resume” etc. -->
      <filter class="solr.ASCIIFoldingFilterFactory"
              preserveOriginal="true"/>
    </analyzer>
  </fieldType>

  <fieldType name="text_phon" class="solr.TextField" positionIncrementGap="100">
    <analyzer>
      <tokenizer class="solr.StandardTokenizerFactory"/>
      <filter class="solr.StopFilterFactory" words="stopwords_prog_en.txt" ignoreCase="true"/>
      <filter class="solr.LowerCaseFilterFactory"/>
      <filter class="solr.PhoneticFilterFactory" encoder="DoubleMetaphone"/>
    </analyzer>
  </fieldType>

  <fieldType name="string" class="solr.StrField" sortMissingLast="true" docValues="true"/>

  <!-- For categorical facets like paradigms -->
  <fieldType name="strings" class="solr.StrField" sortMissingLast="true" docValues="true" multiValued="true"/>

  <!-- For boolean facets -->
  <fieldType name="boolean" class="solr.BoolField" sortMissingLast="true"/>

  <!-- Add this with your other field types -->
  <fieldType name="pdate" class="solr.DatePointField" docValues="true"/>

  <dynamicField name="*" type="text_en_prog" indexed="true" stored="true"/>

  <field name="url"      type="string"  indexed="true"  stored="true" required="true"/>
  <field name="title"    type="title_en"  indexed="true"  stored="true"/>
  <field name="document" type="text_en_prog"  indexed="true"  stored="true" large="true"/>

  <!-- meta fileds -->
  <field name="paradigm" type="strings" indexed="true" stored="true" multiValued="false"/>
  <field name="first_appeared" type="string" indexed="true" stored="true"/>
  <field name="stable_release" type="string" indexed="true" stored="true"/>
  <field name="stable_release_date" type="pdate" indexed="true" stored="true"/>
  <field name="typing_discipline" type="strings" indexed="true" stored="true"/>
  <field name="influenced_by" type="strings" indexed="true" stored="true" multiValued="false"/>
  <field name="influenced" type="strings" indexed="true" stored="true" multiValued="false"/>


  <field name="catch_all" type="text_en_prog" stored="true" multiValued="true"/>
  <copyField source="*" dest="catch_all"/>
  <field name="phonetic_field" type="text_phon" indexed="true"/>
  <copyField source="document" dest="phonetic_field"/>

</schema>
```

## Final Solar `solrconfig.xml`

```xml
<?xml version='1.0' encoding='UTF-8' ?>
<config>
  <luceneMatchVersion>8.9.0</luceneMatchVersion>
  <codecFactory class="solr.SchemaCodecFactory"/>
  <schemaFactory class="solr.ClassicIndexSchemaFactory"/>
  <requestHandler name="/select" class="solr.SearchHandler" default="true">
  <lst name="defaults">
    <str name="echoParams">explicit</str>
    <str name="wt">json</str>
    <str name="indent">true</str>
  </lst>
  </requestHandler>
  <requestHandler name="/select_spell" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="df">spellcheck_field</str>
      <str name="spellcheck.dictionary">default</str>
      <str name="spellcheck.dictionary">wordbreak</str>
      <str name="spellcheck">on</str>
      <str name="spellcheck.extendedResults">true</str>
      <str name="spellcheck.count">10</str>
      <str name="spellcheck.alternativeTermCount">5</str>
      <str name="spellcheck.maxResultsForSuggest">10</str>
      <str name="spellcheck.collate">true</str>
      <str name="spellcheck.collateExtendedResults">true</str>
      <str name="spellcheck.maxCollationTries">10</str>
      <str name="spellcheck.maxCollations">5</str>
    </lst>
    <arr name="last-components">
      <str>spellcheck</str>
    </arr>
  </requestHandler>
  <searchComponent name="spellcheck" class="solr.SpellCheckComponent">
    <str name="queryAnalyzerFieldType">string</str>
    <lst name="spellchecker">
      <str name="name">default</str>
      <str name="field">spellcheck_field</str>
      <str name="classname">solr.DirectSolrSpellChecker</str>
      <str name="distanceMeasure">internal</str>
      <float name="accuracy">0.3</float>
      <int name="maxEdits">2</int>
      <int name="minPrefix">1</int>
      <int name="maxInspections">10</int>
      <int name="minQueryLength">1</int>
      <float name="maxQueryFrequency">0.01</float>
    </lst>
    <lst name="spellchecker">
      <str name="name">wordbreak</str>
      <str name="classname">solr.WordBreakSolrSpellChecker</str>
      <str name="field">spellcheck_field</str>
      <str name="combineWords">true</str>
      <str name="breakWords">true</str>
      <int name="maxChanges">10</int>
    </lst>
  </searchComponent>
</config>
```

## Vector Search und Embedding

In diesem Abschnitt wird die Implementierung von semantischen Suchfunktionen und Embedding-Technologien im Projekt beschrieben.

### Embedding-Modelle

In den Notebooks `embeddings.ipynb` und `embeddings_v2.ipynb` führen wir Experimente mit Sentence-Transformer-Modellen durch, insbesondere mit den Snowflake Arctic Embed Modellen:

- **Modellauswahl**: Ich verwenden verschiedene `Snowflake` Modelle
- **Verarbeitung langer Dokumente**: Implementierung von Text-Chunking-Techniken zur effizienten Verarbeitung umfangreicher Dokumente
- **Vektorrepräsentation**: Die Modelle generieren Embeddings von Texten, um semantische Ähnlichkeiten über reine Schlüsselwortabgleiche hinaus zu erfassen

### Architektur der semantischen Suche

Der semantische Suchablauf funktioniert wie folgt:

1. **Text-Chunking**: Dokumente werden in überlappende Abschnitte unterteilt (mit `MAX_TOK=2048` und `STRIDE=256`)
2. **Vektor-Embedding**: Jeder Abschnitt wird in eine Vektorraumdarstellung eingebettet
3. **Abfrageverarbeitung**: Benutzeranfragen werden als "Query"-Prompts formatiert und mit demselben Modell eingebettet
4. **Ähnlichkeitsberechnung**: Die Kosinus-Ähnlichkeit zwischen Abfragevektoren und Dokumentvektoren wird berechnet
5. **Ergebnisranking**: Ergebnisse werden nach Ähnlichkeitswert sortiert und dem Benutzer präsentiert

### Implementierung hybrider Suche

Das Notebook `hybrid_search.ipynb` implementiert eine ausgereifte hybride Suchfunktionalität:

- **Dualer Ansatz**: Kombiniert lexikalische (schlüsselwortbasierte) und semantische (vektorbasierte) Suchmethoden
- **Integrationsstrategie**: Nutzt Solr's Boolean Query Parser, um beide Suchmethodologien effektiv zu verbinden
- **Verbesserte Präzision**: Liefert genauere Ergebnisse durch die Nutzung der Stärken beider Ansätze

### Leistungsbewertung

Die F1-Evaluierung in `f1-calc.ipynb` wurde erweitert, um die Leistung der hybriden Suche zu messen:

- **Vergleichsanalyse**: Benchmarkt traditionelle Suchmethoden gegen hybride Suchansätze
- **Metrikberechnung**: Berechnet Precision, Recall und F1-Scores für verschiedene Abfragetypen
- **Visuelle Darstellung**: Präsentiert Verbesserungen durch vergleichende Metrikvisualisierungen


Die Ergebnisse zeigen, dass die semantische/hybride Suche bei komplexen natürlichsprachlichen Abfragen zwar mehr Treffer liefert als die rein lexikalische Suche – insbesondere in Fällen, in denen die Standardsuche keine oder nur wenige Ergebnisse zurückgibt. Allerdings fällt auf, dass die hybride Suche aktuell oft sehr viele (teils fast alle) Dokumente als Treffer zurückliefert. Hier besteht noch Optimierungspotenzial, um die Treffermenge gezielter und präziser einzugrenzen.

## Projektstruktur und Ordnerübersicht

Im Folgenden wird beschrieben, welche Dateien und Notebooks sich in welchem Ordner befinden und wofür sie verwendet werden.

### /home/bfh/irsed/daten/

- **prog_lang.json**  
  Enthält die gescrapten und strukturierten Informationen zu den Programmiersprachen.
- **ProgLang/temp/**  
  Temporäre Ablage der heruntergeladenen HTML-Dateien von Wikipedia.

### /home/bfh/irsed/notebooks/

- **scraper.ipynb**  
  Notebook zum Scrapen und Verarbeiten der Wikipedia-Daten zu Programmiersprachen. Hier werden die Daten gesammelt, gefiltert, gespeichert und als JSON exportiert.
- **f1-calc.ipynb**  
  Notebook zur Definition des Goldstandards, Auswertung der Suchqualität (Precision, Recall, F1-Score) und Visualisierung der Ergebnisse für verschiedene Suchabfragen und Solr-Cores.
- **ranking-functional.ipynb**  
  Notebook zur Evaluation und Visualisierung des Rankings für funktionale Programmiersprachen.
- **ranking-object.ipynb**  
  Notebook zur Evaluation und Visualisierung des Rankings für objektorientierte Programmiersprachen.
- **scraper_meta.ipynb**  
  Notebook zum Scrapen und Auswerten der Metadaten (Infoboxen) der Programmiersprachen von Wikipedia.
- **facet.ipynb**  
  Notebook zum Experimentieren mit Facetten-Suchanfragen in Solr.
- **semantic-knowledge-graph.ipynb**  
  Notebook zur Erstellung und Auswertung eines Knowledge Graphs auf Basis der Metadaten (z.B. `influenced_by`).

### /home/bfh/irsed/notebooks/results/

- **results-f1.json**  
  Ergebnisse der F1-Auswertung aus dem Notebook `f1-calc.ipynb`.
- **results-ranking-*.json**  
  Ergebnisse der Ranking-Evaluationen aus den jeweiligen Ranking-Notebooks.

### /home/bfh/irsed/notebooks/gui/

- **gui/**  
  Enthält die Implementierung der grafischen Benutzeroberfläche (GUI) für die Suche und Auswertung.

### Weitere Dateien

- **GoldStandart.xlsx**  
  Excel-Datei mit Goldstandard-Definitionen und Scores für verschiedene Suchabfragen.
- **programming_languages_influence.html**  
  Visualisierung des Knowledge Graphs als HTML-Datei.

---

**Hinweis:**  
Alle relevanten Notebooks und Skripte befinden sich im Ordner `/home/bfh/irsed/notebooks/`. Die gesammelten und verarbeiteten Daten liegen im Unterordner `/home/bfh/irsed/daten/`. Die GUI-Komponenten sind im Unterordner `/home/bfh/irsed/notebooks/gui/` zu finden.

## Ai Disclaimer

Die meinst Scripts wurden von llm generiert und übernommen und manuell verbessert.