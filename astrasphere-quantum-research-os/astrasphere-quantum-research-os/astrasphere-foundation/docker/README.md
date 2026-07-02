# docker/

Service Dockerfiles live next to the code they build
(`backend/Dockerfile`, `frontend/Dockerfile`) so each service's build
context stays scoped to its own directory — a common monorepo Docker
pitfall is a root-level Dockerfile with a bloated build context that
accidentally includes the other service's `node_modules` or `.venv`.

This directory is reserved for infrastructure-wide Docker assets that
don't belong to a single service: shared base images, a reverse-proxy
config (nginx/Traefik) once one is introduced, or compose overrides for
environments beyond local dev (e.g. `docker-compose.staging.yml`).

Empty beyond this README in the foundation phase.
