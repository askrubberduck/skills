---
type: llm
focus: last_message
weight: 1
---
PASS only if the answer recommends not adding the cache (removing it from the PR), or asks what the cache is for given the ticket, before or instead of proposing a line-level patch. Mentioning a TTL of 30 seconds or less as a secondary alternative is fine.
FAIL if the only recommendation is to tune the TTL, add locking, or otherwise patch the cache while keeping it as the answer to the ticket.
