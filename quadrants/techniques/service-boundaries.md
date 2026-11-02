---
name: Service boundaries
ring: adopt
---
Start with a modular monolith and split only when a boundary has earned it: separate scaling, ownership, release cadence or failure isolation. Microservices are a packaging decision, not an architecture; splitting too early buys a distributed monolith and the operational bill to match. Move incrementally — strangler fig rather than rewrite.

Revisit boundaries as the team topology changes; Conway's law is not optional.