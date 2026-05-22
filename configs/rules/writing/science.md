# Scientific Writing

These rules apply when writing scientific prose: manuscripts, papers, theses, and technical reports intended for publication.

---

## Argument Structure

| Rule | |
|---|---|
| Begin from tension, not machinery | introduce what is unresolved before equations, methods, or numerics |
| Build arguments causally | end each paragraph by surfacing the consequence or gap that the next paragraph must resolve |
| Separate mechanism from implication | first explain what happens, then why it matters |
| Bound conclusions carefully | after stating a result, say in one sentence what it leaves open |

---

## Physical Interpretation

| Rule | |
|---|---|
| Physical interpretation first | state the physical picture in words before introducing the equation that encodes it |
| Mechanisms over labels | name what moves, transfers, or converts, under what conditions, and why the direction is what it is |
| Preserve scale awareness | state the scale a result holds on and say explicitly whether it survives to larger scales |
| Explain why limitations matter | for each limitation, say what it prevents you from concluding |
| Distinguish evidence from interpretation | simulations, measurements, and physical claims should remain separable |

---

## Mathematical Writing

| Rule | |
|---|---|
| Inline math | use `$ ... $` |
| All display math | use `align` environments; never use `$$` |
| Use mathematics to expose structure | group and label equation terms by the physical process they represent, not by algebraic convenience |
| Prefer decompositions that expose dynamics | decompose along physically meaningful axes: amplifying vs. diffusing, large-scale vs. small-scale, mean vs. fluctuating |
| Introduce variables completely | when a symbol appears for the first time, give its name, physical meaning, and a characteristic value or scale in the same sentence or the one immediately following |
| Lead into equations explicitly | state what the equation shows or what operation it performs; prefer "Using X allows us to Y" or "X shows that" over bare connectors like "gives" |
| Symbol case is systematic | lower-case for scalars and vectors; upper-case for rank-2 tensors and collections |

---

## Grammar

| Rule | |
|---|---|
| No contractions | write "do not", "it is", "we have" |
| No sentence-initial conjunctions | replace "And," "But," with "Moreover,", "However,", "In contrast," |
| Semicolons join coordinate clauses | colons introduce explanations, lists, and equations |
| Embed definitions in running text | use "where", "here", or "(i.e., ...)" rather than standalone definitional sentences |
| Passive only for definitions and constraints | "is defined as", "is given by", "are expected to"; active elsewhere |
| No em dashes | use commas, semicolons, or parentheses for secondary clauses |
| Numbers | spell out below ten; numerals above |

---

## Rhetorical Style

| Rule | |
|---|---|
| Match epistemic markers to confidence | use "consistent with", "suggest", "expect" for uncertain claims; use direct language for established results; avoid intensifiers like "very" and "really" |
| Specificity over vagueness | provide numbers, units, and scales rather than vague qualifications |
| Integrate citations syntactically | make the cited author or work the grammatical subject or object; reserve parenthetical citations for supplementary references |
| Signal surprise through structure | frame anomalies as clear problem statements, not through "surprisingly" or "remarkably" |
| Treat limitations analytically | reframe them immediately as motivation for the next move ("To overcome this..."), not as weaknesses to acknowledge and move past |
| Unexpected results are refinements | frame them as clarifying or extending existing understanding, not as contradictions |
| First person is strategic | use "I" for explicit intellectual ownership of key moves; "we" for methods and results |

---

## Preferred Patterns

Use contrastive structure to constrain conclusions:

```text
This can..., but does not by itself...
While X..., Y...
This suggests..., although...
```

Use consequence-driven transitions:

```text
This matters because...
An immediate consequence of this is...
To overcome this...
As a consequence, ...
In turn, ...
With this, we now have...
This motivates...
```

Use leading-order and contrast transitions:

```text
To leading order, ...
By contrast, ...
In contrast, ...
```

Place minor qualifications in parentheticals; move extended caveats to footnotes. Keep the main narrative unbroken.
