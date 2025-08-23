from datetime import datetime
from decimal import Decimal

from app.schemas import Author, User, Book, Review, OrderItem, Order

if __name__ == "__main__":
    # Create an author instance
    jrr_tolkien = Author(
        id=1,
        first_name="J.R.R.",
        last_name="Tolkien",
        biography="A fantasy author best known for The Lord of the Rings."
    )
    print(f"Created Author: {jrr_tolkien.last_name}")

    # Create a user instance
    john_doe = User(
        id=101,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password_hash="hashed_password_string",
        created_at=datetime.now()
    )
    print(f"Created User: {john_doe.email}")

    # Create a book instance
    the_hobbit = Book(
        id=1001,
        title="The Hobbit",
        author_id=jrr_tolkien.id,
        isbn="978-0-618-05326-7",
        price=Decimal("15.99"),
        published_date=datetime(1937, 9, 21),
        description="A fantasy novel by J.R.R. Tolkien.",
        stock_quantity=50
    )
    print(f"Created Book: {the_hobbit.title} by {the_hobbit.author_id}")

    # Create a review instance
    review_one = Review(
        id=2001,
        book_id=the_hobbit.id,
        user_id=john_doe.id,
        rating=5,
        comment="An absolute classic!",
        created_at=datetime.now()
    )
    print(f"Created Review with rating: {review_one.rating}")

    # Create an order and order item
    order_item_1 = OrderItem(
        id=3001,
        order_id=4001,
        book_id=the_hobbit.id,
        quantity=1,
        price_at_purchase=the_hobbit.price
    )

    customer_order = Order(
        id=4001,
        user_id=john_doe.id,
        order_date=datetime.now(),
        total_price=order_item_1.price_at_purchase * order_item_1.quantity,
        status="Shipped",
        items=[order_item_1]
    )

    print(f"Created Order for user ID {customer_order.user_id} with a total price of ${customer_order.total_price}")

    # Pydantic validation handles bad data automatically.
    # try:
    #     bad_review = Review(
    #         id=2002,
    #         book_id=the_hobbit.id,
    #         user_id=john_doe.id,
    #         rating=6, # This will raise a ValidationError
    #         created_at=datetime.now()
    #     )
    # except Exception as e:
    #     print(f"Failed to create invalid review. Error: {e}")
