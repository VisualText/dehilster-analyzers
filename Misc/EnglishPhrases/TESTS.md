# Test suite & iterative findings

30 challenging multi-sentence texts live in [input/tests/](input/tests/), each
aimed at one linguistic phenomenon. Running the analyzer over them drives the
improvements below.

Run them all and print a compact one-line-per-sentence summary with
`c:\tmp\run_tests.py` (parses each `phrases.txt`).

## Adjustments made (driven by the tests)

| # | Test that exposed it | Problem | Fix |
|---|----------------------|---------|-----|
| 1 | 10, 25 proper nouns | Unknown words (Mary, Monday, Chicago) were dropped | `lookup`: unknown word → `_noun` |
| 2 | 7, 17 modals/copula | `can swim`, `is reading` → verb became a noun | `disambig` rule 3b: `aux (+adv)* + ambig-verb → verb` |
| 3 | 6, 17, 20 copula | be-forms (`is/are/was/were`) absent from dictionary (`are`→noun) | new `kb/user/en-copula.dict` with `pos=copula` |
| 4 | (lemma request) | no base form recorded | `root=be` in en-copula.dict; `buildKB` records `root` in the KB/JSON |
| 5 | 8, 22, 28 conj | `than`, `because` (conj-only, non-function words) → noun | `lookup`: conj-only word → `_conj` |
| 6 | 24, 28 punctuation | commas split appositives / subordinate clauses into separate "sentences" | `sentences`: allow `, ; : '` inside a `_SENT` |

## Status per test (after the fixes)

Good: 02, 03, 06, 07, 08, 09, 11, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 30
(noun phrases, verb groups with modals/auxiliaries/copula, prepositional
phrases, passives, coordination, comparatives, existentials, multiple PPs,
relative `who`, and the complex paragraph all chunk correctly).

## Known limitations (future adjustments)

These need either richer tokenization or clause-level grammar and are left as
documented next steps:

* **Possessive `'s`** (04): tokenized as three tokens `John ' s`; the apostrophe
  breaks the NP. Needs a possessive pass or tokenizer setting so `John's` is one
  unit.
* **Gerund subjects** (05): `Running fast burns ...` — a gerund as the clause
  subject is read as an adjective string. Needs gerund-subject handling.
* **Imperatives** (29): a sentence-initial bare verb (`Open the door`) defaults
  to a noun because there is no subject.
* **`to` preposition vs infinitive** (03): `walked to school` makes `school` a
  verb because `to` is always treated as the infinitive marker.
* **`that` determiner vs conj** (14): sentence-initial `That house` tags `that`
  as a conjunction rather than a demonstrative determiner.
* **Phrasal-verb particles** (01): `turned off` keeps `off` as a preposition
  rather than a verb particle.

These are expected boundaries of a phrase chunker; the structure produced is
still usable for each.

## Long-sentence suite ([input/long/](input/long/))

Ten texts of five long, multi-clause sentences each (narrative, history,
science, legal, mystery, travel, business, nature, school, everyday). Run with
`python c:\tmp\run_tests.py long`.

### Further adjustments (driven by the long texts)

| Test that exposed it | Problem | Fix |
|----------------------|---------|-----|
| science, history | ambiguous main verbs after a subject (`explosion scatters`, `kings built`, `planets form`) read as nouns | broadened rule 8: subject + ambiguous-verb + **any complement** (prep/adv/det/pron/adj) → verb |
| science | a verb separated from its subject by an adverb (`universe steadily builds`) stayed a noun | rule 8 now skips intervening adverbs |
| narrative | `the other boats` broke the NP (`other` is tagged a pronoun) | rule 9: a pronoun between a determiner and a nominal → adjective |

### Remaining hard cases in long texts

* **Chained ambiguities** where both the subject and verb are noun/verb/adj
  ambiguous (`a bright star runs`, `gas and dust gather`): the premodifier
  chain consumes them before the verb can be found.
* **noun + ambiguous-verb compounds** (`this process repeats`) are read as
  noun-noun compounds; distinguishing them needs verb subcategorization.
* Sentence-initial subordinators (`When`, `Although`, `Once`) tag inconsistently
  as adverb vs conjunction.

These need clause-level grammar (subject/predicate spans) rather than local
chunking rules.

## Round 3: possessives and relative clauses

| Test that exposed it | Problem | Fix |
|----------------------|---------|-----|
| 04 possessive | `John's brother` tokenized as `John ' s`, fragmenting the NP | `possessive` pass: flag the possessor, `excise` the `' s` (matches `_noun`/`_ambig` possessors) |
| 02, 30 relative clauses | a relative clause's verb merged with the main verb | `relpro` tags `who/which/whom/whose` (and `that` only after a noun); `relclause` groups `relpro … VG …` into `_RELCLAUSE` |

`who/that` relative vs `that` complementizer are distinguished by context
(`the woman that called` → relative clause; `I think that she left` → conj).

### Clause segmentation — scope note

Full clause segmentation was scoped down to relative clauses because the general
case requires resolving three hard ambiguities that need real grammar, not
local rules:

* preposition vs subordinator (`before the walk` vs `before he left`);
* coordinating `and` joining noun phrases vs joining clauses (`dog and cat` vs
  `he ran and she left`);
* detecting where a clause *ends*, not just where it starts.

Relative clauses avoid all three (the relative pronoun is unambiguous and the
clause ends at its own verb group), so that slice was implemented first.

## Round 4: subordinate clauses

`subord` tags the reliably-subordinating conjunctions (`when`, `although`,
`while`, `because`, `if`, `unless`, `whereas`, `though`) and `subclause` groups
`sub … VG …` into `_SUBCLAUSE`, bounded at its own verb group like a relative
clause:

* `[When the rain stopped], the children played outside`
* `she slept early [because she was tired]`
* `birds darted between the ferns [while a curious deer watched the strangers]`

The preposition-ambiguous subordinators (`after`, `before`, `as`, `since`) are
left untagged so `before the walk` stays a PP; their clausal use needs a
look-ahead for a full clause.

## Round 5: coordinate clauses (and the verbs around "and")

`coordtag` distinguishes clause-coordinating `and/but/or` (predicate before,
new subject after) from phrase-coordinating (`the dog and the cat`); `coord`
then wraps each main clause in a `_CLAUSE`:

* `[he ran] and [she walked]` -> two `_CLAUSE`s
* `the dog and the cat slept` -> stays one clause (NP coordination)
* `[While the afternoon passed] the children played] and [the dogs chased the ball]` -> nested clauses

Two coupled disambiguation fixes were needed so the coordinator test sees the
right phrases:

| Problem | Fix |
|---------|-----|
| a verb after `and` sharing the subject became a noun (`stopped and ate`, `packed and drove`), which also caused a false clause split | rule 3c: `and/but/or` + ambiguous-verb + object -> verb |
| `the dogs chased the ball`, `this process repeats again` read `chased`/`repeats` as compound nouns | compound rule now skips a verb-capable word that is followed by an object/adjunct (det/pron/adj/adv) |

VP coordination with a shared subject (`turned off the light and looked up the
answer`) correctly stays within one clause (the coordinator is not followed by a
new subject).

## Round 6: dictionary-driven subordinators (incl. preposition-ambiguous)

Subordinators now live in a dictionary (`kb/user/en-subord.dict`) rather than
hard-coded word lists, with two flags:

* `subord=1` — reliably a subordinator (`when`, `because`, `while`, `although`,
  `if`, `once`, …) → always tagged `_sub`;
* `subordprep=1` — also a preposition (`after`, `before`, `as`, `since`,
  `until`) → tagged `_sub` only when a full clause (subject + verb) follows.

So context decides the preposition-ambiguous ones:

* `before the morning sun rose over the hills` → `_SUBCLAUSE`
* `before the long walk home` → `_PP` (no verb → stays a preposition)
* `After the long flight landed` → `_SUBCLAUSE`
* `After several long meetings, the members agreed` → not a clause (`after` + NP)

This follows the same dictionary pattern as `en-copula.dict`: lexical facts live
in dictionaries, the passes read the flags.

## Round 7: dictionary-driven relative pronouns & coordinators

Following the same pattern, the remaining hard-coded word lists moved into
dictionaries:

* `kb/user/en-relpro.dict` — `who/whom/which/whose` flagged `relpro=1`; `relpro`
  now keys off the flag. This also fixed `which`/`whose`, which arrive as
  determiners (`interrogativeDeterminers`) and were missed by the old
  pronoun-only rule — e.g. `The ancient city [which had survived countless wars]`.
* `kb/user/en-coord.dict` — `and/but/or/nor/yet` flagged `coord=1`; `coordtag`
  and the VP-coordination rule read the flag.

The VP-coordination verb rule was also tightened to require a clear object
(determiner/pronoun) after the coordinator, so NP coordination with an adjective
(`wars and long droughts`) is no longer misread as a second verb, while
`stopped … and ate our lunch` still resolves the verb.

## Round 8: predicate repair (every clause needs a verb)

The three documented edge cases — chained ambiguity (`a bright star runs`),
gerund subjects (`Running fast burns`), and imperatives (`Open the door`) — are
the same problem: a sentence left with **no verb** because the real verb
collapsed into a noun.  The `predicate` pass repairs it:

* **Imperative** — sentence opens with a verb-capable noun directly followed by
  an object (`Open the door`, `Take the book and read it`, `Bring me the coffee`)
  → promote the opening word.  All imperatives now resolve their verb(s).
* **Declarative** — a verb-capable noun immediately after the subject head
  (only adjectives/adverbs between) is the verb (`Water flows ...`,
  `a bright star runs ...`).  It stops at the first preposition/conjunction so a
  noun inside the subject's own modifiers is never grabbed
  (`clouds of gas and dust ...` is left alone rather than promoting `gas`).

It only fires on verbless sentences, so regression risk is low (the main
paragraph and both suites are unchanged).

Still hard (documented): a verbless **subordinate** clause inside a sentence
that already has a main verb (`When a bright star runs ..., the pressure can
...`) — the per-sentence check sees `can` and skips; and gerund subjects whose
gerund was tagged an adjective (`Running fast`).

## Round 9: coordinator needs a verb before it

`coordtag` was rewritten as a scan that tags a coordinator `_cc` only when a
verb group has already appeared in the current clause (the first clause must
have its own predicate) and a noun phrase follows.  This removes the false split
on phrase coordination inside a subject:

* `These drifting clouds of gas and dust gather` → one clause (no verb before
  `and`) — previously mis-split at `gas`/`dust`.
* `She is reading and they are sleeping` → still two clauses (verb before `and`,
  subject after).
* `dog and cat slept` / `stopped … and ate the lunch` → stay plain conjunctions.

## Round 10: per-clause predicate repair

The `predicate` pass now runs after the relative/subordinate markers are tagged
and treats commas, subordinators (`_sub`) and relative pronouns (`_relpro`) as
clause boundaries, so each clause is repaired on its own.  A verbless
subordinate clause is now fixed even when the main clause has a verb:

* `When a bright star runs out of fuel, the pressure can fail` → the subordinate
  clause gets its verb (in the clean case where the subject head is a noun).

A "chained" repair (for subjects whose head was mis-tagged an adjective, e.g.
`a bright [star]/adj [runs]/noun`) was implemented and then **removed**: the
pattern `det adj noun` is identical whether the noun is the verb (`star runs`)
or the subject head with a later verb (`These drifting clouds ... gather`), so
it mis-fired.  `star runs out of its fuel` is left as a known edge.

## Round 11: questions & dialogue ([input/dialogue/](input/dialogue/))

Ten texts of questions and quoted speech (yes/no and wh-questions, tag
questions, dialogue attribution, indirect questions).

Works well: auxiliary inversion (`Did the old dog bark?`, `Is the water safe?`,
`Are you ready?`), wh-determiners (`Which road ...`, `Whose coat ...`), dialogue
verbs (`said`, `replied`, `whispered`), and lemmas throughout (`[do]`, `[be]`,
`[child]`).

Adjustments driven by this folder:

* **Interrogative vs relative** — sentence-initial `Who/Which/Whose` were being
  grouped as relative clauses (`Who took the ball` → RELCLAUSE).  `relpro` now
  tags a relative pronoun only when a noun precedes it (`the man who ...`), so
  interrogatives stay question words.
* **`like` as verb** — `lookup` no longer pins a preposition-tagged word that is
  ALSO a verb (`like`); it stays open-class, so `You like coffee` / `Would you
  like coffee` read `like` as a verb while `looks like X` can still be a prep.
* **`Let` / quotes** — `predicate` now skips stray quotation marks, so the
  imperative check sees the real first word: `He replied, "Let us walk home"` →
  `Let` is a verb.

Noted (not yet fixed): `Please` imperatives (`Please open ...`), and a few
dictionary stem glitches (`us`→`u`, `pass`→`pas`, `lives`→`life`) that come
straight from `en-full.dict`.

> Tooling note: the runner (`c:\tmp\run_tests.py`) now auto-detects the latest
> installed `dehilster.nlp-*` engine — a VS Code extension update had changed the
> path (3.1.23 → 3.1.24) and was causing silent stale output.

## Summary of clause handling

The analyzer now produces a sentence → clause → phrase → word hierarchy:
relative clauses (`_RELCLAUSE`), subordinate clauses (`_SUBCLAUSE`), and
coordinated main clauses (`_CLAUSE` … `_cc` … `_CLAUSE`), over NP/PP/VG chunks
with disambiguated parts of speech, lemmas, and possessive marking — all dumped
to `phrases.txt`, the KB (`.kbb`), and `output.json`.
