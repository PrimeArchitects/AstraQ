"""Unit tests for password hashing and JWT token utilities — no DB, no network."""

import uuid

import pytest
from app.core.security import (
    InvalidTokenError,
    TokenPurpose,
    create_access_token,
    create_email_verification_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    fingerprint,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_is_not_the_plaintext(self) -> None:
        hashed = hash_password("SecurePass123")
        assert hashed != "SecurePass123"

    def test_verify_correct_password(self) -> None:
        hashed = hash_password("SecurePass123")
        assert verify_password("SecurePass123", hashed) is True

    def test_verify_incorrect_password(self) -> None:
        hashed = hash_password("SecurePass123")
        assert verify_password("WrongPassword1", hashed) is False

    def test_same_password_hashes_differently_each_time(self) -> None:
        """Bcrypt salts automatically — two hashes of the same password
        must differ, or salting is broken."""
        hash_a = hash_password("SecurePass123")
        hash_b = hash_password("SecurePass123")
        assert hash_a != hash_b
        assert verify_password("SecurePass123", hash_a)
        assert verify_password("SecurePass123", hash_b)


class TestTokens:
    def test_access_token_round_trips(self) -> None:
        user_id = uuid.uuid4()
        token = create_access_token(user_id)
        payload = decode_token(token, TokenPurpose.ACCESS)
        assert payload["sub"] == str(user_id)
        assert payload["purpose"] == "access"

    def test_refresh_token_carries_session_id(self) -> None:
        user_id = uuid.uuid4()
        session_id = uuid.uuid4()
        token = create_refresh_token(user_id, session_id)
        payload = decode_token(token, TokenPurpose.REFRESH)
        assert payload["sid"] == str(session_id)

    def test_wrong_purpose_is_rejected(self) -> None:
        """A token minted for one purpose must never validate for another —
        this is what stops an email-verification link from being replayed
        as an access token."""
        user_id = uuid.uuid4()
        access_token = create_access_token(user_id)
        with pytest.raises(InvalidTokenError):
            decode_token(access_token, TokenPurpose.REFRESH)

    def test_tampered_token_is_rejected(self) -> None:
        user_id = uuid.uuid4()
        token = create_access_token(user_id)
        tampered = token[:-4] + "abcd"
        with pytest.raises(InvalidTokenError):
            decode_token(tampered, TokenPurpose.ACCESS)

    def test_email_verification_token_binds_email(self) -> None:
        user_id = uuid.uuid4()
        token = create_email_verification_token(user_id, "person@example.com")
        payload = decode_token(token, TokenPurpose.EMAIL_VERIFICATION)
        assert payload["email"] == "person@example.com"

    def test_password_reset_token_binds_hash_fingerprint(self) -> None:
        user_id = uuid.uuid4()
        fp = fingerprint("$2b$12$somehash")
        token = create_password_reset_token(user_id, fp)
        payload = decode_token(token, TokenPurpose.PASSWORD_RESET)
        assert payload["pwfp"] == fp

    def test_fingerprint_is_deterministic_and_short(self) -> None:
        fp1 = fingerprint("$2b$12$somehash")
        fp2 = fingerprint("$2b$12$somehash")
        assert fp1 == fp2
        assert len(fp1) == 16

    def test_fingerprint_changes_with_input(self) -> None:
        assert fingerprint("hash-a") != fingerprint("hash-b")
