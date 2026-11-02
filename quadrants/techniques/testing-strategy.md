---
name: Testing strategy
ring: adopt
---
Decide the shape deliberately: many fast unit and component tests, a thin end-to-end layer, and contract tests at service boundaries so two services can agree without a full environment. Flaky tests are a defect in the pipeline, not a nuisance to retry.

Adopt as a position. The runners and frameworks matter far less than where each kind of test sits, what it is allowed to touch, and who owns it when it breaks.