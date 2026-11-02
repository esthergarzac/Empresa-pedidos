from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)

FIXED_NOW = datetime(2026, 10, 30, 12, 0, tzinfo=UTC)


def test_admin_can_cancel_new_order_of_another_user():
    # Arrange: el pedido es del usuario 1 y lo cancela el admin (usuario 99)
    created_at = FIXED_NOW - timedelta(hours=48)

    # Act
    allowed = can_cancel("NEW", 1, 99, True, created_at, FIXED_NOW)

    # Assert
    assert allowed is True


def test_owner_denied_at_exactly_24_hours():
    # Arrange: el límite es estricto (< 24 h), así que 24 h exactas se rechazan
    created_at = FIXED_NOW - timedelta(hours=24)

    # Act
    allowed = can_cancel("NEW", 1, 1, False, created_at, FIXED_NOW)

    # Assert
    assert allowed is False


def test_owner_allowed_just_before_24_hours():
    # Arrange: un minuto antes del límite
    created_at = FIXED_NOW - timedelta(hours=23, minutes=59)

    # Act
    allowed = can_cancel("NEW", 1, 1, False, created_at, FIXED_NOW)

    # Assert
    assert allowed is True