---
name: Terraform
ring: adopt
---
Default for provisioning cloud infrastructure: declarative, reviewable and state-tracked. OpenTofu is the hedge if licensing becomes a problem.

I'd avoid it for dynamic, high-churn resources better managed from the application or from Kubernetes manifests.
