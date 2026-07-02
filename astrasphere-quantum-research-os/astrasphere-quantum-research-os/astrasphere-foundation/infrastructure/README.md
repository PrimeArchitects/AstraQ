# infrastructure/

Infrastructure-as-code for deploying AstraSphere beyond a developer's
laptop. `docker-compose.yml` at the repo root covers local development;
this directory is reserved for staging/production provisioning
(Terraform, Kubernetes manifests, or a managed-platform config) once a
target cloud is chosen.

- **environments/local/** — placeholder; local dev uses the root
  `docker-compose.yml` directly.
- **environments/staging/** — reserved for staging infra definitions.
- **environments/production/** — reserved for production infra
  definitions.

No cloud resources are defined yet. This is intentionally empty beyond
structure until a deployment target is selected.
