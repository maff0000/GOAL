"""Policy test for GOLD-AUD-D acceptance criterion 7: gateway ordering.

Guarantee: the typed gateway precedes accepted TRON integration (O-A) and
precedes PAPER proof (O-B), enforced two ways and each obligation separately.

* Graph: ``backlog/backlog.yaml`` makes the typed gateway a transitive ancestor
  of each consumer. Neither consumer lists the gateway directly, so the check
  uses transitive ancestry, not direct edges.
* Text: the lane D ``ORDERING.md`` still states both halves of the ordering
  sentence, plus the Gate A statement, the gate table row and the readings.

Identifier mapping. ``TRON-T2`` is used as the identifier for "accepted TRON
integration". That is stricter than the ORDERING.md prose, which separates the
adapter-versus-fake-backend work (INC-11, not accepted integration) from the
adapter-against-a-real-gateway work (INC-14); both halves live in TRON-T2.
``PAPER-E2E-001`` reaches the gateway through both ``TRON-T2`` and
``GOLD-MVP-001``, so severing one consumer edge alone does not break O-B; the
mutation tests remove both.

Real files are only read. Mutations act on in-memory copies. The approval half
of "exists and approved" has no graph representation and is not asserted.

Text half strategy: exact pinning, deliberately. A word blacklist cannot close
the class of qualifications, cancellations and removals, so the text half does
not try to recognise weakening. After HTML comments and fenced code blocks are
stripped from the body of section 1 and whitespace is normalised, obligation
item 1 (from its marker to where item 2 begins) must equal CANONICAL_ITEM_1
exactly. Any prefix, suffix, extra sentence, qualification, comment-wrapping,
code-fencing or removal fails. ``check_tron_half`` and ``check_paper_half``
remain independently failing checks with their own messages, and the
weakening-word guard stays as an extra defence; ``check_ordering_text`` runs
all of them plus the exact-item equality. Consequence: any legitimate
rewording of the obligation must update this policy test in the same governed
change. That friction is the point.
"""

import re

import pytest

from goal_dcp import model
from goal_dcp.model import load_backlog

TYPED_GATEWAY = "MT5-GW-003"  # INC-10, typed allow-list service
ACCEPTED_TRON_INTEGRATION = "TRON-T2"  # INC-14 (second half); see module docstring
PAPER_PROOF = "PAPER-E2E-001"  # INC-17
ORDERING_PATH = (
    model.REPO_ROOT / "audits/2026-10-15/gold-mvp/lanes/GOLD-AUD-D/ORDERING.md"
)

O_A = "O-A typed gateway before accepted TRON integration"
O_B = "O-B typed gateway before PAPER proof"

GATEWAY_CHAIN_EDGE_1 = (ACCEPTED_TRON_INTEGRATION, "MT5-GW-004")
GATEWAY_CHAIN_EDGE_2 = ("MT5-GW-004", TYPED_GATEWAY)


# --------------------------------------------------------------------- graph


def real_graph():
    return {i.id: tuple(i.depends_on) for i in load_backlog().items}


def ancestors(graph, node):
    seen = set()
    stack = list(graph.get(node, ()))
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(graph.get(cur, ()))
    return seen


def without_edges(graph, *edges):
    out = dict(graph)
    for src, dst in edges:
        out[src] = tuple(d for d in out[src] if d != dst)
    return out


def check_ids_exist(graph):
    for ident in (TYPED_GATEWAY, ACCEPTED_TRON_INTEGRATION, PAPER_PROOF):
        assert ident in graph, f"backlog item {ident} is missing"


def check_obligation(graph, label, consumer):
    found = ancestors(graph, consumer)
    assert TYPED_GATEWAY in found, (
        f"{label}: {TYPED_GATEWAY} is not a transitive ancestor of {consumer}; "
        f"ancestors found: {sorted(found)}"
    )


def check_no_inversion(graph):
    gw = ancestors(graph, TYPED_GATEWAY)
    for consumer in (ACCEPTED_TRON_INTEGRATION, PAPER_PROOF):
        assert consumer not in gw, (
            f"inversion: {consumer} is an ancestor of {TYPED_GATEWAY}"
        )


def test_policy_ids_exist_in_backlog():
    check_ids_exist(real_graph())


def test_o_a_typed_gateway_precedes_accepted_tron_integration():
    graph = real_graph()
    check_obligation(graph, O_A, ACCEPTED_TRON_INTEGRATION)
    print(O_A, "ancestors:", sorted(ancestors(graph, ACCEPTED_TRON_INTEGRATION)))


def test_o_b_typed_gateway_precedes_paper_proof():
    graph = real_graph()
    check_obligation(graph, O_B, PAPER_PROOF)
    print(O_B, "ancestors:", sorted(ancestors(graph, PAPER_PROOF)))


def test_no_inversion_gateway_is_not_downstream_of_consumers():
    check_no_inversion(real_graph())


# --------------------------------------------------------------------- text


def normalised(text):
    return " ".join(text.split())


def read_ordering():
    return ORDERING_PATH.read_text(encoding="utf-8")


OBLIGATIONS_HEADING = "## 1. The two binding obligations"
_HEADING_RE = re.compile(
    r"^" + re.escape(OBLIGATIONS_HEADING) + r"[ \t]*$", re.MULTILINE
)
_NEXT_H2_RE = re.compile(r"^## ", re.MULTILINE)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_ITEM_MARKER_RE = re.compile(r"^[ \t]*(?:(\d+)[.)]|[-*+])[ \t]+")

CANONICAL_ITEM_1 = (
    "The typed gateway must exist and be approved before accepted TRON "
    "integration or PAPER proof."
)

# Words that negate, weaken, reverse or make optional. Applied to the whole
# obligation sentence and to each clause of it.
_WEAKENING_RE = re.compile(
    r"\b(?:not|never|no|neither|nor|cannot|need|optional|optionally|without|"
    r"unless|except|after|afterwards|following|may|might|could|should|can|"
    r"skip|skipped|waive|waived|ignore|ignored|later|once|until|while|when|"
    r"whenever|if)\b|n't",
    re.IGNORECASE,
)
_CLAUSE_SPLIT_RE = re.compile(r",|;|:|\band\b|\bor\b|\bbut\b", re.IGNORECASE)

TRON_PHRASE = "typed gateway must exist and be approved before accepted TRON integration"
# "before" immediately governing PAPER proof, directly, or as the second item
# of the same "before accepted TRON integration or PAPER proof" list, and the
# sentence ending there (nothing may follow PAPER proof).
_PAPER_TAIL_RE = re.compile(
    r"\bbe approved before (?:accepted TRON integration or )?PAPER proof\.?$"
)


def strip_fenced_blocks(text):
    """Remove fenced code blocks (``` or ~~~); an unclosed fence runs to the end."""
    out, fence = [], None
    for line in text.splitlines(keepends=True):
        if fence is None:
            m = _FENCE_OPEN_RE.match(line)
            if m:
                fence = m.group(1)
            else:
                out.append(line)
        else:
            body = line.strip()
            if body and set(body) == {fence[0]} and len(body) >= len(fence):
                fence = None
    return "".join(out)


def strip_invisible(text):
    """Drop what a reader never sees: fenced code blocks, then HTML comments."""
    return _COMMENT_RE.sub("", strip_fenced_blocks(text))


def obligations_section(text):
    """Visible body of '## 1. The two binding obligations', or None.

    Fenced code blocks and HTML comments are stripped from the body.
    """
    m = _HEADING_RE.search(text)
    if m is None:
        return None
    rest = text[m.end():]
    n = _NEXT_H2_RE.search(rest)
    return strip_invisible(rest[: n.start()] if n else rest)


def obligation_items(section):
    """Split the section into (marker_number_or_None, normalised_text) segments.

    A new segment starts at each list-item marker line; text before the first
    marker is segment 0 with no marker.
    """
    segs = [[None, []]]
    for line in section.splitlines():
        m = _ITEM_MARKER_RE.match(line)
        if m:
            segs.append([m.group(1) or "-", [line[m.end():]]])
        else:
            segs[-1][1].append(line)
    return [(num, normalised(" ".join(lines))) for num, lines in segs]


def locate_item_1(text, half="ordering"):
    """Normalised text of obligation item 1, or an AssertionError (fail closed)."""
    section = obligations_section(text)
    assert section is not None, (
        f"{half} half: section {OBLIGATIONS_HEADING!r} not found"
    )
    items = obligation_items(section)
    hits = [
        i
        for i, (_, t) in enumerate(items)
        if "typed gateway" in t.lower() and "must exist" in t.lower()
    ]
    assert hits, (
        f"{half} half: no visible obligation item in section 1 states the "
        "typed gateway ordering (removed, commented out or fenced?)"
    )
    assert len(hits) == 1, (
        f"{half} half: {len(hits)} items state the typed gateway ordering; "
        "exactly one is allowed"
    )
    i = hits[0]
    assert items[i][0] in (None, "1"), (
        f"{half} half: ordering item carries marker {items[i][0]!r}, expected 1"
    )
    assert i + 1 < len(items) and items[i + 1][0] == "2", (
        f"{half} half: obligation item 2 does not follow item 1"
    )
    return items[i][1]


def ordering_sentences(text):
    """Obligation sentences found ONLY inside the obligations section."""
    section = obligations_section(text)
    if section is None:
        return None
    return [
        s
        for s in re.split(r"(?<=[.!?])\s+", normalised(section))
        if "typed gateway" in s and "must exist" in s
    ]


def weakening_in(sentence):
    """The first weakening/negation found in the sentence or any clause."""
    for part in [sentence] + _CLAUSE_SPLIT_RE.split(sentence):
        m = _WEAKENING_RE.search(part)
        if m:
            return m.group(0)
    return None


def _obligation_sentences_or_fail(text, half):
    sents = ordering_sentences(text)
    assert sents is not None, (
        f"{half} half: section {OBLIGATIONS_HEADING!r} not found"
    )
    assert sents, (
        f"{half} half: no sentence in section 1 states the typed gateway ordering"
    )
    for s in sents:
        w = weakening_in(s)
        assert w is None, f"{half} half: obligation sentence weakened by {w!r}: {s!r}"
    return sents


def check_exact_item(text):
    """Obligation item 1 must be exactly the canonical sentence, nothing else."""
    item = locate_item_1(text, "exact-item")
    assert item == CANONICAL_ITEM_1, (
        "exact-item: obligation item 1 is not the canonical text; "
        f"expected {CANONICAL_ITEM_1!r}, found {item!r}"
    )


def check_ordering_text(text):
    """Both halves, then the exact-item equality that every variant must meet."""
    check_tron_half(text)
    check_paper_half(text)
    check_exact_item(text)


def check_nonempty(text):
    assert normalised(text), "ORDERING.md is empty"


def check_tron_half(text):
    for s in _obligation_sentences_or_fail(text, "TRON"):
        assert TRON_PHRASE in s, f"ordering sentence lacks the TRON half: {s!r}"


def check_paper_half(text):
    for s in _obligation_sentences_or_fail(text, "PAPER"):
        assert "must exist" in s and _PAPER_TAIL_RE.search(s), (
            f"ordering sentence lacks the PAPER half: {s!r}"
        )


def check_gate_a(text):
    lines = text.splitlines()
    assert any("GATE A" in ln and "typed gateway" in ln for ln in lines), (
        "no GATE A line naming the typed gateway"
    )
    assert any(
        "Typed gateway exists and is approved" in ln
        and "INC-14" in ln
        and "INC-17" in ln
        for ln in lines
    ), "gate table row (Typed gateway exists and is approved ... INC-14 ... INC-17) missing"


def check_readings(text):
    lines = text.splitlines()
    assert any("PAPER-E2E-001" in ln and "PAPER proof" in ln for ln in lines), (
        "no line associating PAPER-E2E-001 with PAPER proof"
    )
    assert any(
        "INC-14" in ln and "first accepted TRON integration" in ln for ln in lines
    ), "no line associating INC-14 with first accepted TRON integration"


def test_ordering_file_exists_and_is_nonempty():
    assert ORDERING_PATH.is_file(), f"{ORDERING_PATH} missing"
    check_nonempty(read_ordering())


def test_ordering_states_tron_half():
    check_tron_half(read_ordering())


def test_ordering_states_paper_half():
    check_paper_half(read_ordering())


def test_ordering_item_1_is_exactly_canonical():
    check_exact_item(read_ordering())
    check_ordering_text(read_ordering())


def test_ordering_carries_gate_a_statement_and_table_row():
    check_gate_a(read_ordering())


def test_ordering_names_the_readings():
    check_readings(read_ordering())


# ---------------------------------------------------------------- mutations


def test_m1_drop_gw004_to_gw003_breaks_both_obligations():
    g = without_edges(real_graph(), GATEWAY_CHAIN_EDGE_2)
    with pytest.raises(AssertionError, match="O-A"):
        check_obligation(g, O_A, ACCEPTED_TRON_INTEGRATION)
    with pytest.raises(AssertionError, match="O-B"):
        check_obligation(g, O_B, PAPER_PROOF)


def test_m2_drop_tron_t2_to_gw004_breaks_both_obligations():
    g = without_edges(real_graph(), GATEWAY_CHAIN_EDGE_1)
    with pytest.raises(AssertionError, match="O-A"):
        check_obligation(g, O_A, ACCEPTED_TRON_INTEGRATION)
    with pytest.raises(AssertionError, match="O-B"):
        check_obligation(g, O_B, PAPER_PROOF)


def test_m3_drop_both_paper_consumer_edges_breaks_only_o_b():
    g = without_edges(
        real_graph(),
        (PAPER_PROOF, ACCEPTED_TRON_INTEGRATION),
        ("GOLD-MVP-001", ACCEPTED_TRON_INTEGRATION),
    )
    with pytest.raises(AssertionError, match="O-B"):
        check_obligation(g, O_B, PAPER_PROOF)
    check_obligation(g, O_A, ACCEPTED_TRON_INTEGRATION)  # still holds


@pytest.mark.parametrize(
    "edge",
    [
        (PAPER_PROOF, ACCEPTED_TRON_INTEGRATION),
        ("GOLD-MVP-001", ACCEPTED_TRON_INTEGRATION),
    ],
)
def test_positive_control_single_paper_consumer_edge_is_redundant(edge):
    g = without_edges(real_graph(), edge)
    check_obligation(g, O_B, PAPER_PROOF)
    check_obligation(g, O_A, ACCEPTED_TRON_INTEGRATION)


def test_m4_deleted_gateway_item_fails_id_check():
    g = real_graph()
    del g[TYPED_GATEWAY]
    with pytest.raises(AssertionError, match=TYPED_GATEWAY):
        check_ids_exist(g)


def test_m5_reversed_edge_fails_anti_inversion():
    g = real_graph()
    g[TYPED_GATEWAY] = g[TYPED_GATEWAY] + (ACCEPTED_TRON_INTEGRATION,)
    with pytest.raises(AssertionError, match="inversion"):
        check_no_inversion(g)


def test_m6_text_drop_paper_proof_fails_paper_half_only():
    text = read_ordering().replace(" or PAPER proof.", ".", 1)
    assert text != read_ordering()
    with pytest.raises(AssertionError, match="PAPER half"):
        check_paper_half(text)
    check_tron_half(text)


def test_m7_text_drop_accepted_tron_integration_fails_tron_half_only():
    text = read_ordering().replace("accepted TRON integration or ", "", 1)
    assert text != read_ordering()
    with pytest.raises(AssertionError, match="TRON half"):
        check_tron_half(text)
    check_paper_half(text)


def test_m8_text_drop_gate_a_line_fails_gate_check():
    text = "\n".join(
        ln for ln in read_ordering().splitlines() if "GATE A" not in ln
    )
    with pytest.raises(AssertionError, match="GATE A"):
        check_gate_a(text)


def test_m9_empty_text_fails_every_text_check():
    for check in (
        check_nonempty,
        check_tron_half,
        check_paper_half,
        check_gate_a,
        check_readings,
    ):
        with pytest.raises(AssertionError):
            check("")


# ------------------------------------------- text mutations (auditor findings)

REAL_SENTENCE = (
    "The typed gateway must exist and be approved before accepted TRON "
    "integration or PAPER proof."
)


def with_sentence(replacement):
    text = read_ordering()
    assert REAL_SENTENCE in text, "real ORDERING.md sentence changed; update test"
    return text.replace(REAL_SENTENCE, replacement, 1)


def test_positive_control_real_file_passes_text_checks():
    text = read_ordering()
    assert len(ordering_sentences(text)) == 1
    check_tron_half(text)
    check_paper_half(text)


@pytest.mark.parametrize(
    "tail",
    [
        "before accepted TRON integration, and need not precede PAPER proof.",
        "before accepted TRON integration, never before PAPER proof.",
        "before accepted TRON integration or PAPER proof is not required.",
        "before accepted TRON integration, and after PAPER proof.",
        "before accepted TRON integration, and only after PAPER proof.",
        "before accepted TRON integration, but PAPER proof may precede it.",
        "before accepted TRON integration and PAPER proof is optional.",
    ],
)
def test_m10_weakened_or_reversed_paper_clause_fails_paper_half(tail):
    text = with_sentence("The typed gateway must exist and be approved " + tail)
    with pytest.raises(AssertionError, match="PAPER half"):
        check_paper_half(text)


@pytest.mark.parametrize(
    "tail",
    [
        "after accepted TRON integration or PAPER proof.",
        "only after accepted TRON integration or PAPER proof.",
        "before accepted TRON integration is not required, nor before PAPER proof.",
        "before accepted TRON integration is optional or PAPER proof.",
        "before accepted TRON integration, never.",
    ],
)
def test_m11_weakened_or_reversed_tron_clause_fails_tron_half(tail):
    text = with_sentence("The typed gateway must exist and be approved " + tail)
    with pytest.raises(AssertionError, match="TRON half"):
        check_tron_half(text)


def test_m12_obligation_only_in_unrelated_section_fails_both_halves():
    text = with_sentence("The gateway is discussed in section 2.")
    marker = "- INC-11 and INC-12 do not wait"
    assert marker in text
    text = text.replace(marker, "- " + REAL_SENTENCE + "\n" + marker, 1)
    assert REAL_SENTENCE in text  # equivalent sentence exists, but in section 4
    with pytest.raises(AssertionError, match="TRON half"):
        check_tron_half(text)
    with pytest.raises(AssertionError, match="PAPER half"):
        check_paper_half(text)


def test_m13_missing_section_heading_fails_both_halves():
    text = read_ordering().replace(OBLIGATIONS_HEADING, "## 1. Something else", 1)
    with pytest.raises(AssertionError, match="TRON half"):
        check_tron_half(text)
    with pytest.raises(AssertionError, match="PAPER half"):
        check_paper_half(text)


def test_m14_extra_weak_duplicate_in_section_1_fails():
    text = with_sentence(
        REAL_SENTENCE
        + " The typed gateway must exist and be approved before accepted "
        "TRON integration, and need not precede PAPER proof."
    )
    with pytest.raises(AssertionError, match="PAPER half"):
        check_paper_half(text)


# ------------------------------- exact-item mutations (second audit findings)


def assert_fails_closed(text):
    """The variant must fail the exact-item check and the combined gate."""
    with pytest.raises(AssertionError):
        check_exact_item(text)
    with pytest.raises(AssertionError):
        check_ordering_text(text)


def test_positive_control_exact_item_tolerates_rewrap_and_invisible_markup():
    wrapped = (
        "The typed gateway   must exist and be approved\n   before accepted "
        "TRON integration\n   or PAPER proof."
    )
    check_ordering_text(with_sentence(wrapped))
    check_ordering_text(
        with_sentence("<!-- note -->" + REAL_SENTENCE.replace("approved", "approved<!-- x -->"))
    )
    text = read_ordering().replace(
        "## 2. Order", "## 2. Order\n<!-- a comment -->\n```\nfenced\n```", 1
    )
    check_ordering_text(text)


@pytest.mark.parametrize(
    "prefix",
    ["Generally, ", "In principle, ", "For most work, ", "Where possible, "],
)
def test_m15_qualifying_prefix_fails_exact_item(prefix):
    body = REAL_SENTENCE[0].lower() + REAL_SENTENCE[1:]
    assert_fails_closed(with_sentence(prefix + body))


def test_m16_sentence_wrapped_in_html_comment_fails():
    assert_fails_closed(with_sentence("<!-- " + REAL_SENTENCE + " -->"))


def test_m16b_multiline_html_comment_wrap_fails():
    assert_fails_closed(with_sentence("<!--\n" + REAL_SENTENCE + "\n-->"))


def test_m17_sentence_deleted_leaving_only_comment_fails():
    assert_fails_closed(with_sentence("<!-- removed by CA -->"))


def test_m17b_sentence_deleted_outright_fails():
    assert_fails_closed(with_sentence(""))


@pytest.mark.parametrize("fence", ["```", "~~~", "````"])
def test_m18_sentence_in_fenced_code_block_fails(fence):
    assert_fails_closed(with_sentence(f"{fence}text\n{REAL_SENTENCE}\n{fence}"))


def test_m18b_unclosed_fence_fails():
    assert_fails_closed(with_sentence("```\n" + REAL_SENTENCE))


@pytest.mark.parametrize(
    "follow",
    [
        "The CA may waive this.",
        "PAPER proof may nonetheless proceed first.",
        "Both are advisory.",
        "Accepted TRON integration is not blocked by it.",
        "Non-blocking.",
        "Ordering is advisory only.",
    ],
)
@pytest.mark.parametrize("sep", [" ", "\n", "\n\n"], ids=["same-line", "next-line", "new-para"])
def test_m19_cancelling_follow_up_in_item_1_fails(follow, sep):
    assert_fails_closed(with_sentence(REAL_SENTENCE + sep + follow))


def test_m19b_cancelling_follow_up_passes_old_guard_but_not_exact_item():
    # Shows why exact pinning is needed: no weakening word, halves still pass.
    text = with_sentence(REAL_SENTENCE + " Both are mandatory only on Tuesdays.")
    check_tron_half(text)
    check_paper_half(text)
    with pytest.raises(AssertionError, match="exact-item"):
        check_exact_item(text)


def test_m20_qualifying_prefix_passes_halves_but_not_exact_item():
    text = with_sentence("Generally, the typed gateway must exist and be approved "
                         "before accepted TRON integration or PAPER proof.")
    check_tron_half(text)
    check_paper_half(text)
    with pytest.raises(AssertionError, match="exact-item"):
        check_exact_item(text)


def test_m21_item_2_marker_removed_swallows_item_2_and_fails():
    text = read_ordering().replace("\n2. Diagnostic", "\nDiagnostic", 1)
    assert text != read_ordering()
    assert_fails_closed(text)
