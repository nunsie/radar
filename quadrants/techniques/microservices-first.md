---
name: Microservices first
ring: hold
---
Splitting into services before the boundaries are known. You pay the distributed-systems tax — network failures, partial failure, versioning, observability, deployment coordination — before you get any of the benefits, and you usually get a distributed monolith. Prefer a modular monolith until a boundary earns its own deployment.

Revisit per context when separate scaling, ownership or failure isolation is a measured need rather than an aspiration.