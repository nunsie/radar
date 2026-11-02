---
name: Progressive delivery
ring: trial
---
Decouple release from deploy further than feature flags: canary and blue/green rollouts, automated rollback, and fault injection so a bad change is contained to a fraction of traffic. Continuous delivery gets the change out; progressive delivery decides how much blast radius it gets.

Trial: the mechanics are well understood, but doing them well needs good telemetry and automation, and testing in production only works when you can observe and reverse quickly.