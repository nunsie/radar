---
name: Docker
ring: adopt
---
Default way to package and run anything, dev and prod. The image is the unit of deployment, and Compose is the default way to run that image plus its dependencies locally — if a stack cannot run under Compose, that is usually a smell worth fixing.

Avoid only where a serverless deploy or a single compiled binary is genuinely simpler.