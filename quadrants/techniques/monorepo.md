---
name: Monorepo
ring: adopt
---
Default for related projects: atomic changes, shared tooling, one CI.

Adopt when the projects genuinely change together; split when they don't. A caching task runner (Turborepo and friends) earns its place once the graph is big enough to page in — below that, plain scripts and CI caching do the job.