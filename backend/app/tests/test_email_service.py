"""Tests for email service."""
import pytest

from app.services.email import create_order_confirmation_email


def test_create_order_confirmation_email():
    """Test that order confirmation email is created with correct content."""
    # Arrange
    user_email = "test@example.com"
    user_name = "John Doe"
    order_id = 12345
    order_date = "2024-01-15 10:30:00 UTC"
    total_price = "99.98"
    items = [
        {
            "title": "The Great Gatsby",
            "quantity": 2,
            "price_at_purchase": "10.99",
        },
        {
            "title": "1984",
            "quantity": 1,
            "price_at_purchase": "12.50",
        },
    ]

    # Act
    message = create_order_confirmation_email(
        user_email=user_email,
        user_name=user_name,
        order_id=order_id,
        order_date=order_date,
        total_price=total_price,
        items=items,
    )

    # Assert
    assert message["To"] == user_email
    assert message["Subject"] == f"Order Confirmation #{order_id} - Kohyli Bookstore"
    assert "Kohyli Bookstore" in message["From"]
    
    # Get the message parts
    parts = message.get_payload()
    assert len(parts) == 2  # text and html parts
    
    # Check plain text part
    text_content = parts[0].get_payload()
    assert user_name in text_content
    assert str(order_id) in text_content
    assert order_date in text_content
    assert total_price in text_content
    assert "The Great Gatsby" in text_content
    assert "1984" in text_content
    
    # Check HTML part
    html_content = parts[1].get_payload()
    assert user_name in html_content
    assert str(order_id) in html_content
    assert order_date in html_content
    assert total_price in html_content
    assert "The Great Gatsby" in html_content
    assert "1984" in html_content
    assert "<table" in html_content  # HTML table structure
    assert "<!DOCTYPE html>" in html_content


def test_create_order_confirmation_email_empty_items():
    """Test order confirmation email with no items (edge case)."""
    # Arrange
    user_email = "test@example.com"
    user_name = "Jane Smith"
    order_id = 1
    order_date = "2024-01-15 10:30:00 UTC"
    total_price = "0.00"
    items = []

    # Act
    message = create_order_confirmation_email(
        user_email=user_email,
        user_name=user_name,
        order_id=order_id,
        order_date=order_date,
        total_price=total_price,
        items=items,
    )

    # Assert
    assert message["To"] == user_email
    assert message["Subject"] == f"Order Confirmation #{order_id} - Kohyli Bookstore"
    
    # Get the message parts
    parts = message.get_payload()
    assert len(parts) == 2  # text and html parts
    
    # Verify basic structure is still present
    html_content = parts[1].get_payload()
    assert user_name in html_content
    assert str(order_id) in html_content
    assert total_price in html_content
