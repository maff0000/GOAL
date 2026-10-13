PROSE-001 boilerplate that mentions every required word and states none of them.

Proves: the validator reads section headings, not keywords. This file is
deliberately headingless — not one line in it is an ATX heading — so every one
of the five requirements is unmet, including identity, even though the id
`PROSE-001` and the words purpose, scope, acceptance criteria and approval all
appear in it as running prose.

The purpose of this work is broad. The scope of this work is broad. The
acceptance criteria for this work are broad, and approval was obtained. None
of those four sentences is a section, and a grep-shaped check that looked for
the words rather than the headings would accept this document as a PID.

Note what is NOT asserted here: that prose is worthless. A PID is mostly
prose. What the rule requires is that the five things be findable — a reader
handed this file cannot tell where the scope statement ends and the acceptance
criteria begin, because there is no structure to tell them apart.
