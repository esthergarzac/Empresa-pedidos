import pytest

from src.domain import CustomerHasDebt, Order


def test_vip_discount():
    o = Order(100, vip=True)
    assert o.confirm() == 85
    assert o.status == "CONFIRMED"

def test_regular_no_discount():
    assert Order(100).confirm() == 100

def test_customer_debt():
    with pytest.raises(CustomerHasDebt):
        Order(100).confirm(customer_debt=50)

@pytest.mark.parametrize("total", [0, -1])
def test_invalid_total(total):
    with pytest.raises(ValueError):
        Order(total).confirm()

def test_vip_discount_on_200():
    # Arrange
    order = Order(200, vip=True)

    # Act
    amount = order.confirm()

    # Assert
    assert amount == 170
    assert order.status == "CONFIRMED"


def test_regular_customer_no_discount_on_200():
    # Arrange
    order = Order(200)

    # Act
    amount = order.confirm()

    # Assert
    assert amount == 200
    assert order.status == "CONFIRMED"

def test_cannot_confirm_twice():
    # Arrange
    order = Order(100)
    order.confirm()

    # Act + Assert
    with pytest.raises(ValueError, match="already confirmed"):
        order.confirm()