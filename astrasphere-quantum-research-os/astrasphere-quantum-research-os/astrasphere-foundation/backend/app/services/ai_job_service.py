"""Placeholder AI job submission — records intent only; no job is
executed. A future async worker will pick these up and update status."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import NotFoundError
from app.models.ai_job import AIJob
from app.models.user import User
from app.repositories.ai_job_repository import AIJobRepository
from app.schemas.ai_job import AIJobCreate
from app.services.base import BaseService


class AIJobService(BaseService):
    def __init__(self, ai_job_repo: AIJobRepository) -> None:
        self.ai_jobs = ai_job_repo

    async def list_for_owner(self, user: User, offset: int = 0, limit: int = 20) -> list[AIJob]:
        return await self.ai_jobs.list_for_owner(user.id, offset, limit)

    async def get_owned(self, user: User, job_id: uuid.UUID) -> AIJob:
        job = await self.ai_jobs.get_for_owner(job_id, user.id)
        if job is None:
            raise NotFoundError("AI job not found.")
        return job

    async def submit_job(self, user: User, payload: AIJobCreate) -> AIJob:
        job = AIJob(owner_id=user.id, job_type=payload.job_type, payload=payload.payload)
        job = await self.ai_jobs.create(job)
        await record_activity(
            self.ai_jobs.session,
            user_id=user.id,
            action="create",
            resource_type="ai_job",
            resource_id=str(job.id),
            extra_data={"job_type": job.job_type},
        )
        return job
