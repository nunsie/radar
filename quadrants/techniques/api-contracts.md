---
name: API contracts & lifecycle
ring: adopt
---
Design the interface first and treat it as a product: explicit contracts (OpenAPI, Protobuf), consumer-driven contract tests, a real versioning policy, and an actual deprecation and sunset process. Adding is safe; changing and removing is where callers break.

Adopt for anything with more than one consumer or a life longer than one team's attention span. The cost is the discipline of not breaking callers, which is far cheaper than coordinated releases.