import { type FC, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useApi } from "../context/ApiContext";
import type { Order, Book } from "../Client";

/**
 * Local type for items displayed in the thank you page.
 * Each item includes book fields plus an optional quantity.
 */
type OrderItem = Book & { quantity?: number };

/**
 * Displays a thank you page for a recently created order.
 * Expects navigation state: { order: Order }.
 * If state is missing, redirects to /me.
 */
export const ThankYou: FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const api = useApi();

    // The created order may be passed via navigation state
    const stateOrder = (location.state as any)?.order as Order | undefined;

    const [order, setOrder] = useState<Order | null>(stateOrder ?? null);
    const [items, setItems] = useState<OrderItem[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        if (!order) {
            // No order in state => redirect back to user page
            navigate("/me");
            return;
        }

        const fetchItems = async () => {
            try {
                // The orders endpoint now returns order + items/books
                const resp = await api.orders.getOrder(order.id);
                const orderData = resp.data ?? {};

                // Items may live under `items` or `books` (or be a direct array)
                const itemsFromResp = orderData.items ?? orderData.books ?? [];

                // Normalize items into OrderItem (Book + quantity)
                const normalized: OrderItem[] = (itemsFromResp as any[]).map((it: any) => {
                    // If item shape is { book: {...}, quantity }, extract book
                    if (it && typeof it === "object" && it.book) {
                        return { ...(it.book as Book), quantity: it.quantity ?? 1 };
                    }

                    // Otherwise assume it's a Book-like object possibly with quantity or qty
                    return { ...(it as Book), quantity: (it && (it.quantity ?? it.qty)) ?? 1 };
                });

                // Update order fields (remove nested items/books keys) to keep order up-to-date
                const { items: _items, books: _books, ...orderFields } = orderData;

                setOrder(orderFields as Order);
                setItems(normalized);
            } catch (err) {
                console.error("Failed to fetch order items:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchItems();
    }, [order, api, navigate]);

    if (!order) {
        return null;
    }

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-3xl font-extrabold text-slate-800 mb-4">Thank you for your order!</h1>
                <p className="text-sm text-slate-600 mb-6">Order #{order.id} — Placed on {new Date(order.order_date).toLocaleString()}</p>
                <div className="mb-6">
                    <p className="font-semibold">Order Summary</p>
                    <p className="text-slate-700">Total: €{Number(order.total_price).toFixed(2)}</p>
                    <p className="text-sm text-slate-500">Status: {order.status}</p>
                </div>

                <h2 className="text-xl font-semibold mb-3">Items</h2>
                {loading ? (
                    <p>Loading items...</p>
                ) : items.length === 0 ? (
                    <p>No items found for this order.</p>
                ) : (
                    <ul className="space-y-3">
                        {items.map((b) => (
                            <li key={b.id} className="flex items-center justify-between border rounded-md p-3">
                                <div className="flex items-center">
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
                                </div>
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
                        View your orders
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ThankYou;
