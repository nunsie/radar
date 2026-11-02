---
name: Shared database across services
ring: hold
---
A database read and written directly by several services. It couples their schemas and releases, makes independent deploys a fiction, and turns every migration into a cross-team negotiation. Integrate through an interface or a published event stream instead.

Revisit only as a deliberate, temporary migration step — never as the steady state.