"""
Transactional email abstraction — architecture placeholder, same pattern
as `app/ai/provider.py`. No real email provider (SES, Postmark, etc.) is
wired up in this phase; `ConsoleEmailSender` logs the message instead,
so verification/reset links are visible during local development and in
test output rather than silently vanishing.
"""

from abc import ABC, abstractmethod

import structlog

logger = structlog.get_logger("email")


class EmailSender(ABC):
    @abstractmethod
    async def send(self, *, to: str, subject: str, body: str) -> None: ...


class ConsoleEmailSender(EmailSender):
    """Logs the email instead of sending it. Swap for a real provider
    (SES/Postmark/etc.) behind this same interface when one is chosen."""

    async def send(self, *, to: str, subject: str, body: str) -> None:
        logger.info("email_dispatched_dev_mode", to=to, subject=subject, body=body)


def get_email_sender() -> EmailSender:
    return ConsoleEmailSender()
