"""Email service for sending order confirmation emails."""

import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from textwrap import dedent
from typing import List, Dict, Any

import aiosmtplib

from app.config import email_settings

logger = logging.getLogger(__name__)


def create_order_confirmation_email(
    user_email: str,
    user_name: str,
    order_id: int,
    order_date: str,
    total_price: str,
    items: List[Dict[str, Any]],
) -> MIMEMultipart:
    """
    Create an HTML email for order confirmation.

    Args:
        user_email: Recipient email address
        user_name: User's full name
        order_id: Order ID
        order_date: Order date string
        total_price: Total order price
        items: List of items in the order with book details

    Returns:
        MIMEMultipart email message
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Order Confirmation #{order_id} - Kohyli Bookstore"
    message["From"] = (
        f"{email_settings.SMTP_FROM_NAME} <{email_settings.SMTP_FROM_EMAIL}>"
    )
    message["To"] = user_email

    # Create plain text version
    text_content = dedent(f"""
        Dear {user_name},

        Thank you for your order!

        Order ID: {order_id}
        Order Date: {order_date}

        Items:
    """).strip()

    for item in items:
        text_content += f"\n- {item.get('title', 'Unknown')} x {item.get('quantity', 0)} @ ${item.get('price_at_purchase', '0.00')}"

    text_content += f"\n\nTotal: ${total_price}"
    text_content += "\n\nThank you for shopping with Kohyli Bookstore!"

    # Create HTML version
    items_html = ""
    for item in items:
        items_html += dedent(f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{item.get("title", "Unknown")}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{item.get("quantity", 0)}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">${item.get("price_at_purchase", "0.00")}</td>
            </tr>
        """).strip()

    html_content = dedent(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                <h1 style="color: #2c3e50; margin-top: 0;">Order Confirmation</h1>
                <p>Dear {user_name},</p>
                <p>Thank you for your order! Your purchase has been confirmed.</p>
                
                <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Order ID:</strong> #{order_id}</p>
                    <p><strong>Order Date:</strong> {order_date}</p>
                </div>

                <h2 style="color: #2c3e50;">Order Details</h2>
                <table style="width: 100%; border-collapse: collapse; background-color: white;">
                    <thead>
                        <tr style="background-color: #f8f9fa;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Book</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd;">Quantity</th>
                            <th style="padding: 10px; text-align: right; border-bottom: 2px solid #ddd;">Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_html}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="2" style="padding: 10px; text-align: right; font-weight: bold; border-top: 2px solid #ddd;">Total:</td>
                            <td style="padding: 10px; text-align: right; font-weight: bold; border-top: 2px solid #ddd; color: #27ae60;">${total_price}</td>
                        </tr>
                    </tfoot>
                </table>

                <p style="margin-top: 20px;">Thank you for shopping with Kohyli Bookstore!</p>
            </div>
        </body>
        </html>
    """).strip()

    # Attach both versions
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")
    message.attach(part1)
    message.attach(part2)

    return message


async def send_email(message: MIMEMultipart) -> bool:
    """
    Send an email via SMTP.

    Args:
        message: The email message to send

    Returns:
        True if email sent successfully, False otherwise
    """
    # Skip sending if SMTP credentials are not configured
    if not email_settings.SMTP_USERNAME or not email_settings.SMTP_PASSWORD:
        logger.warning(
            "Email sending skipped: SMTP credentials not configured. "
            "Set SMTP_USERNAME and SMTP_PASSWORD environment variables."
        )
        return False

    try:
        await aiosmtplib.send(
            message,
            hostname=email_settings.SMTP_HOST,
            port=email_settings.SMTP_PORT,
            username=email_settings.SMTP_USERNAME,
            password=email_settings.SMTP_PASSWORD,
            use_tls=email_settings.SMTP_USE_TLS,
        )
        logger.info(f"Email sent successfully to {message['To']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


async def send_order_confirmation_email(
    user_email: str,
    user_name: str,
    order_id: int,
    order_date: str,
    total_price: str,
    items: List[Dict[str, Any]],
) -> bool:
    """
    Send order confirmation email to user.

    Args:
        user_email: Recipient email address
        user_name: User's full name
        order_id: Order ID
        order_date: Order date string
        total_price: Total order price
        items: List of items in the order with book details

    Returns:
        True if email sent successfully, False otherwise
    """
    message = create_order_confirmation_email(
        user_email=user_email,
        user_name=user_name,
        order_id=order_id,
        order_date=order_date,
        total_price=total_price,
        items=items,
    )
    return await send_email(message)
