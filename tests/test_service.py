from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)


def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))


def test_gateway_rejected_vip_200():
    # Arrange
    gateway = Mock()
    gateway.charge.return_value = False
    order = Order(200, vip=True)

    # Act + Assert
    with pytest.raises(RuntimeError, match="payment rejected"):
        OrderService(gateway).checkout(order)

    # Assert: se intentó cobrar con el descuento VIP aplicado (200 - 15% = 170)
    gateway.charge.assert_called_once_with(170)


def test_known_risk_order_stays_confirmed_after_rejected_payment():
    # Arrange
    gateway = Mock()
    gateway.charge.return_value = False
    order = Order(100)

    # Act
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(order)

    # Assert: RIESGO CONOCIDO. El pedido queda CONFIRMED aunque el pago fue rechazado.
    assert order.status == "CONFIRMED"