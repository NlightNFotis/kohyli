import { type FC, useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useApi } from "../context/ApiContext";
import type { Order, Book } from "../Client";

/**
 * Local type for items displayed in an order page.
 * Normalized so each item has book fields plus a quantity.
 */
type OrderItem = Book & { quantity?: number };

/**
 * OrderDetails
 * Shows the details and books for a specific order id from the route param.
 */
export const OrderDetails: FC = () => {
    const { id } = useParams<{ id: string }>();
    const api = useApi();
    const navigate = useNavigate();

    const [order, setOrder] = useState<Order | null>(null);
    const [items, setItems] = useState<OrderItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!id) {
            navigate("/me");
            return;
        }

        const orderId = Number(id);
        const fetch = async () => {
            try {
                const orderResp = await api.orders.getOrder(orderId);
                const orderData = orderResp.data ?? {};

                // The API now returns the order together with the books/items.
                // Support possible keys: `items` or `books`.
                const itemsFromResp = orderData.items ?? orderData.books ?? [];

                // Normalize items into OrderItem (Book + quantity)
                const normalized: OrderItem[] = (itemsFromResp as any[]).map((it: any) => {
                    // If each item is { book: {...}, quantity }, extract book and attach quantity
                    if (it && typeof it === "object" && it.book) {
                        return { ...(it.book as Book), quantity: it.quantity ?? 1 };
                    }

                    // If the item already contains book fields (Book + quantity), keep them
                    return { ...(it as Book), quantity: (it && (it.quantity ?? it.qty)) ?? 1 };
                });

                // Remove nested items/books keys so `order` contains just the order fields
                const { items: _items, books: _books, ...orderFields } = orderData;

                setOrder(orderFields as Order);
                setItems(normalized);
            } catch (err) {
                console.error("Failed to load order details:", err);
            } finally {
                setLoading(false);
            }
        };

        fetch();
    }, [id, api, navigate]);

    if (loading) return <p>Loading order...</p>;
    if (!order) return <p>Order not found.</p>;

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h1 className="text-2xl font-extrabold text-slate-800">Order #{order.id}</h1>
                        <p className="text-sm text-slate-600">Placed on {new Date(order.order_date).toLocaleString()}</p>
                    </div>
                    <div className="text-right">
                        <p className="font-semibold">€{Number(order.total_price).toFixed(2)}</p>
                        <p className="text-sm text-slate-600 capitalize">{order.status}</p>
                    </div>
                </div>

                <h2 className="text-lg font-semibold mb-3">Items</h2>
                {items.length === 0 ? (
                    <p className="text-slate-600">No items found for this order.</p>
                ) : (
                    <ul className="space-y-3">
                        {items.map((b) => (
                            <li key={b.id} className="flex items-center justify-between border rounded-md p-3">
                                <Link
                                    to={`/books/${b.id}`}
                                    className="flex items-center no-underline text-inherit"
                                    aria-label={`View details for ${b.title}`}
                                >
                                    <img
                                        src={
                                            b.cover_image_url ||
                                            `https://placehold.co/100x140/cccccc/ffffff?text=No+Image`
                                        }
                                        alt={`Cover of ${b.title}`}
                                        className="w-16 h-20 object-cover rounded-md shadow-sm mr-4 flex-shrink-0"
                                    />
                                    <div>
                                        <p className="font-medium">{b.title}</p>
                                    </div>
                                </Link>
                                <div className="text-right">
                                    <p className="font-medium">€{Number(b.price).toFixed(2)}</p>
                                    <p className="text-sm text-slate-500">Quantity: {b.quantity ?? 1}</p>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}

                <div className="mt-6">
                    <button
                        onClick={() => navigate("/me")}
                        className="inline-flex items-center justify-center rounded-md border border-transparent bg-sky-600 px-4 py-2 text-white hover:bg-sky-700"
                    >
                        Back to your orders
                    </button>
                </div>
            </div>
        </div>
    );
};

export default OrderDetails;
