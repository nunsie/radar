---
name: Reproducible environments
ring: adopt
---
The same environment from laptop to CI to production, declared in-repo: Docker Compose for the local multi-service stack, dev containers or cloud workspaces for per-task isolation, and Nix where the system itself has to be pinned. It is the real answer to "works on my machine", and the prerequisite for letting new joiners or agents run checks anywhere.

Cost is maintaining the environment definition; worth it as soon as more than one person or machine runs the code. Stop where a serverless deploy or a single compiled binary genuinely needs no environment.