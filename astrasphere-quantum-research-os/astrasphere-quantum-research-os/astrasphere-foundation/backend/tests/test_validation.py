"""Schema-level validation tests — weak passwords, malformed input, no DB needed."""

import pytest
from app.schemas.auth import LoginRequest, RegisterRequest, ResetPasswordRequest
from pydantic import ValidationError


class TestRegisterValidation:
    def test_valid_registration_passes(self) -> None:
        req = RegisterRequest(
            email="person@example.com", password="SecurePass123", display_name="A"
        )
        assert req.email == "person@example.com"

    def test_rejects_invalid_email_format(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(email="not-an-email", password="SecurePass123", display_name="A")

    def test_rejects_password_too_short(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(email="person@example.com", password="Short1", display_name="A")

    def test_rejects_password_without_uppercase(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(email="person@example.com", password="lowercase123", display_name="A")

    def test_rejects_password_without_lowercase(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(email="person@example.com", password="UPPERCASE123", display_name="A")

    def test_rejects_password_without_digit(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(email="person@example.com", password="NoDigitsHere", display_name="A")

    def test_rejects_empty_display_name(self) -> None:
        with pytest.raises(ValidationError):
            RegisterRequest(email="person@example.com", password="SecurePass123", display_name="")


class TestLoginValidation:
    def test_rejects_invalid_email_format(self) -> None:
        with pytest.raises(ValidationError):
            LoginRequest(email="not-an-email", password="anything")

    def test_login_does_not_enforce_password_strength(self) -> None:
        """Login must accept whatever password the user set previously —
        strength rules only apply when a password is being (re)created."""
        req = LoginRequest(email="person@example.com", password="x")
        assert req.password == "x"


class TestResetPasswordValidation:
    def test_rejects_weak_new_password(self) -> None:
        with pytest.raises(ValidationError):
            ResetPasswordRequest(token="sometoken", new_password="weak")
