---
name: Event-driven architecture
ring: trial
---
Async, event-based flows where the coupling and latency profile justify them: an outbox instead of dual writes, sagas for multi-step transactions, idempotent consumers, dead-letter queues and deliberate ordering. Exactly-once delivery is a myth; at-least-once plus idempotency is the real target.

Trial: powerful and easy to get subtly wrong. Adopt per bounded context once you can observe and replay the stream, not as a default for the whole system.