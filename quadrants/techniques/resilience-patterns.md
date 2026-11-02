---
name: Resilience patterns
ring: adopt
---
Assume every remote call fails: timeouts on everything, retries with backoff and jitter, idempotency keys so retries are safe, circuit breakers and bulkheads so one dependency cannot take down the rest, and load shedding or backpressure instead of unbounded queues. Design the degradation path, not just the happy one.

No real cost beyond discipline; the failure mode of skipping it is an outage. Revisit thresholds as traffic and the dependency count grow.