#!/usr/bin/env bash
# Re-runs the negative (absence) searches recorded in RECONCILIATION.md.
# Usage: CLONE_ROOT=<dir holding fresh clones named HELIOS falcon tron HSA DARWIN CER hermes> ./negative-searches.sh
# Read-only: git grep over fixed revisions only. An empty result under a command is the recorded finding.
set -u
: "${CLONE_ROOT:?set CLONE_ROOT}"
run() { echo "## $1"; shift; "$@" 2>&1 | cut -c1-160 | head -${LINES_MAX:-12}; echo "(exit-grep-lines: done)"; }
cd "$CLONE_ROOT"
run "N1 HELIOS 7f7193d: trigger, signing, outbox code" git -C HELIOS grep -n -i -E "outbox|ed25519|hmac|strategy_trigger|signing_key" 7f7193d55475e40583892b94dd461b1b64d6f1ef -- helios
run "N2 HELIOS 7f7193d: any redis or network client import in the package" git -C HELIOS grep -n -E "^\s*(import|from) (redis|socket|requests|httpx|aiohttp|urllib)" 7f7193d55475e40583892b94dd461b1b64d6f1ef -- helios
run "N3 HELIOS 7f7193d: inbox or outbox anywhere" git -C HELIOS grep -n -i -E "inbox|outbox" 7f7193d55475e40583892b94dd461b1b64d6f1ef -- .
run "N4 FALCON 8f218ec: TradingTriggerInbox or TriggerInbox" git -C falcon grep -n -i -E "TradingTriggerInbox|TriggerInbox|trigger_inbox" 8f218ec1b85b932285b042a7b1ae64dbd11eebee -- .
run "N5 TRON main 5577039: inbox or outbox" git -C tron grep -n -i -E "TradingTriggerInbox|TriggerInbox|outbox" 5577039b5db05e70effef72c7e59df14db408419 -- .
run "N6 TRON D1 37d5f00: TradingTriggerInbox or TriggerInbox or outbox" git -C tron grep -n -i -E "TradingTriggerInbox|TriggerInbox|outbox" 37d5f009a080d25930eea37cf8c627bb0f3a1ff4 -- .
run "N7 FALCON 8f218ec: outbox implementation (code, not documents)" git -C falcon grep -n -i -l "outbox" 8f218ec1b85b932285b042a7b1ae64dbd11eebee -- . ':!docs' ':!pids'
run "N8 HSA 279ec18: any code producing the HELIOS package schema version" git -C HSA grep -n -i "helios.strategy_package" 279ec181b5cd78df953671e087e01b7c1190ff96 -- hsa contracts
run "N9 HSA 279ec18: fingerprint or canonical hash of a strategy" git -C HSA grep -n -i -E "fingerprint|canonical_hash|semantic_hash" 279ec181b5cd78df953671e087e01b7c1190ff96 -- hsa contracts
run "N10 DARWIN bf1142b: any JSON Schema file in the tree (the A-007 schema)" bash -c "git -C DARWIN ls-tree -r --name-only bf1142b5be9f6988ec36b60ba3db9022c76a47af | grep -i -E 'schema[^/]*[.]json$|[.]schema[.]json$' || true"
