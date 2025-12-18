"""Background task queue for sending emails using arq (Redis-based)."""

import logging
from typing import List, Dict, Any

from arq import create_pool
from arq.connections import RedisSettings

from app.config import db_settings
from app.services.email import send_order_confirmation_email

logger = logging.getLogger(__name__)


async def send_order_confirmation_task(
    ctx,
    user_email: str,
    user_name: str,
    order_id: int,
    order_date: str,
    total_price: str,
    items: List[Dict[str, Any]],
) -> bool:
    """
    Background task to send order confirmation email.

    This function is executed by the arq worker in the background.

    Args:
        ctx: arq context (automatically provided)
        user_email: Recipient email address
        user_name: User's full name
        order_id: Order ID
        order_date: Order date string
        total_price: Total order price
        items: List of items in the order with book details

    Returns:
        True if email sent successfully, False otherwise
    """
    logger.info(f"Processing order confirmation email for order #{order_id}")

    result = await send_order_confirmation_email(
        user_email=user_email,
        user_name=user_name,
        order_id=order_id,
        order_date=order_date,
        total_price=total_price,
        items=items,
    )

    if result:
        logger.info(f"Order confirmation email sent for order #{order_id}")
    else:
        logger.error(f"Failed to send order confirmation email for order #{order_id}")

    return result


class WorkerSettings:
    """Configuration for arq worker."""

    functions = [send_order_confirmation_task]
    redis_settings = RedisSettings(
        host=db_settings.REDIS_HOST,
        port=db_settings.REDIS_PORT,
        database=db_settings.REDIS_DB,
    )


async def enqueue_order_confirmation_email(
    user_email: str,
    user_name: str,
    order_id: int,
    order_date: str,
    total_price: str,
    items: List[Dict[str, Any]],
) -> None:
    """
    Enqueue an order confirmation email task to be sent in the background.

    Args:
        user_email: Recipient email address
        user_name: User's full name
        order_id: Order ID
        order_date: Order date string
        total_price: Total order price
        items: List of items in the order with book details
    """
    try:
        redis = await create_pool(
            RedisSettings(
                host=db_settings.REDIS_HOST,
                port=db_settings.REDIS_PORT,
                database=db_settings.REDIS_DB,
            )
        )

        job = await redis.enqueue_job(
            "send_order_confirmation_task",
            user_email,
            user_name,
            order_id,
            order_date,
            total_price,
            items,
        )

        logger.info(
            f"Enqueued order confirmation email job {job.job_id} for order #{order_id}"
        )

        await redis.close()
    except Exception as e:
        logger.error(f"Failed to enqueue order confirmation email: {e}")
        # Don't fail the order creation if email queueing fails
