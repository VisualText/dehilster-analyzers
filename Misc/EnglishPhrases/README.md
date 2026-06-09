# English Phrases

A clean, bottom-up parser that breaks English prose into sub-sentence phrases
(noun phrases, verb groups, prepositional phrases) while disambiguating words
that have more than one part of speech.

## How it works

The dictionary lookup (`dicttokz`) tags every token with its candidate parts
of speech from `en-full.dict`, plus a fine-grained closed-class category from
`en-function-words.dict`. The passes then build structure from the bottom up:

| Pass | Purpose |
|------|---------|
| `lookup` | Pin function words (articles, prepositions, pronouns, …) to one part of speech; mark genuinely open-class words `_ambig`. |
| `disambig` | Resolve `_ambig` words from context using English principles (run recursively). |
| `defaults` | Give anything still ambiguous its most likely part of speech. |
| `np` / `pp` / `vg` | Build noun phrases, prepositional phrases and verb groups. |
| `sentences` | Group each sentence's phrases under a `_SENT` node. |
| `buildKB` | Mirror the parse tree into the knowledge base under `sentences`. |
| `kbDisplay` / `output` | Save the KB (`.kbb`), write `phrases.txt`, and dump `output.json`. |

## Disambiguation principles (in `disambig`)

* A word that can be a preposition and is followed by a determiner/pronoun is a **preposition** (`before the walk`).
* `to` + verb and pronoun + verb force a **verb** (`to fall`, `he saw`).
* An adjective-capable word before another nominal is a **prenominal adjective** (`quick brown fox`).
* The word after the last adjective is the **head noun** — adjectives modify nouns (`brown fox`, `heavy books`).
* A determiner + noun + ambiguous noun is a **noun-noun compound** (`the kitchen table`); an `-ing` word there is a participle, not a compound head.
* A noun/pronoun + ambiguous verb + preposition is a **post-nominal verb** (`fox jump over`, `children playing on`).

## Output

* `phrases.txt` — a readable, indented phrase breakdown with each word tagged.
* `output.json` — the same structure as JSON: `sentences → sentence[] → phrase[] (type) → word[] (text, pos)`.
* `sentences.kbb` — the knowledge-base dump.
