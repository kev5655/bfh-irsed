```bash
curl -X POST -H "Content-Type: application/json"   "http://localhost:8983/solr/ProgLang/update/json/docs"   --data-binary @/home/bfh/irsed/daten/ProgLang/prog_lang.json && curl "http://localhost:8983/solr/ProgLang/update?commit=true"
```

```bash
curl -X POST -H "Content-Type: application/json"   "http://localhost:8983/solr/ProgLang24_2/update/json/docs"   --data-binary @/home/bfh/irsed/daten/ProgLang/24/prog_lang.json && curl "http://localhost:8983/solr/ProgLang24_2/update?commit=true"
```


```bash
curl -X POST -H "Content-Type: application/json"   "http://localhost:8983/solr/ProgLang24_5/update/json/docs"   --data-binary @/home/bfh/irsed/daten/ProgLang/24_5/prog_lang.json   && curl "http://localhost:8983/solr/ProgLang24_5/update?commit=true"
```


Index erstellen:

1. Kopieren 1_Hello_World index
2. rm -R data
3. Umbenene des indexes in core.properties
4. Run the Post update both url's




Done:

Ich dachte ich konnt die stop word liste mit ein llm generiern lasse, jedoch hat das nciht funktioinert das wahr der vorschlag:
```bash
url "http://localhost:8983/solr/ProgLang24/terms?terms.fl=catch_all&terms.sort=count&terms.limit=1000&wt=json""
```
```python
import json

# Load the raw Solr terms output
with open('terms_output.json') as f:
    data = json.load(f)

terms = data['terms']['catch_all']

# Convert list like ["term1", freq1, "term2", freq2, ...] into tuples
term_freq_pairs = list(zip(terms[::2], terms[1::2]))

# Sort by frequency descending
term_freq_pairs.sort(key=lambda x: x[1], reverse=True)

# Choose top-k or apply threshold (e.g., frequency > 20)
stopwords = [term for term, freq in term_freq_pairs if freq > 20 and term.isalpha()]

# Save to a .txt stopword list
with open('custom_stopwords.txt', 'w') as f:
    f.write('\n'.join(stopwords))
```


F1 Score berechne problem
Ich habe versucht mit title:Python ein querry abzusetzen das hat aber nicht funktioien nach lnage debugen. Habe ich heraus gefunden das indexieren nicht richtig geklab hat und title als string type whar und nicht als text_en mit dem tokenizer


# Stopwords i have used the Load Term Info and removed all words that related to programming langues

# Python problem with pyhton3, python3.12
zeige von WordDelimiterGraphFilterFactory

# C# hat sich das ranking verbessert aber es kommen immer noch ander sparchen aufsplitung von c# auf c sharp

# C++ problem mit title:"c plus plus" lücke eingefügt

stop word mit top term evaluiert. Manuell durchgegane und entfern was nunötig ist dan am schluss noch ein prüfung mit llm

Refactoring umbauen von mauallen heraus finden der werte zu vol automatischn auswerten. Häte ich schon vie f"ruche machen sollen

Neue evaluerinung der treffer, da funktionle und objeict orienteirung nicht zu 100% richtig wahr, ich es am anfange einfach schlecht bewerted habe

F1 Score mit not filter versucht die scores zu erhöhen

F1 Score versucht zu erhöhen mit paradimag neue key, gescrapet von table in wikipedia



### Ranking

docuemnt:'functional'

ich habe ein set verwenden daruch hate ich immer gleich daten