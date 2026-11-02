---
name: Data architecture & schema evolution
ring: trial
---
Treat data as a product with an owner, a schema and a lifecycle: versioned migrations, backward-compatible schema evolution, data contracts between producers and consumers, and explicit retention, privacy and residency rules. Separate transactional from analytical workloads before reporting queries start hurting production.

Trial while the practices settle per stack; the cost of skipping it compounds every time a schema changes under a live consumer.