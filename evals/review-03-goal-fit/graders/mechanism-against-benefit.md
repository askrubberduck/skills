---
type: llm
focus: last_message
weight: 1
---
The ticket requires prices at most 30 seconds old. The change adds a 300-second cache in front of the quote call and claims it stops stale prices.

PASS only if the answer says the cache works against the stated benefit: a 300-second TTL lets a price be up to five minutes old, so the change makes staleness worse, not better.
FAIL if it treats the cache as delivering fresher prices, or only comments on style, thread safety or maxsize without stating that the mechanism contradicts the ticket.
