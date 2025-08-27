
import { type FC } from "react";
import { useCart } from "../context/CartContext";
import { Button } from "./ui/Button";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useApi } from "../context/ApiContext";

/** Decode a JWT payload (base64url) */
function decodeJwt<T = any>(token?: string): T | null {
    if (!token) return null;
    try {
        const parts = token.split(".");
        if (parts.length < 2) return null;
        const payload = parts[1];
        const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
            Array.prototype.map
                .call(atob(base64), (c: string) => {
                    return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
                })
                .join("")
        );
        return JSON.parse(jsonPayload) as T;
    } catch {
        return null;
    }
}

export const Cart: FC = () => {
    const { cart, clearCart } = useCart();
    const { token } = useAuth();
    const api = useApi();
    const navigate = useNavigate();

    const handleCheckout = async () => {
        if (!token) {
            navigate("/login");
            return;
        }

        // Attempt to extract a user id from the JWT. Support common claim names.
        const payload = decodeJwt<Record<string, any>>(token.access_token);
        const userId =
            payload?.user_id ??
            payload?.sub ??
            payload?.id ??
            payload?.uid ??
            payload?.userId;

        if (!userId) {
            alert("Unable to determine user id from token. Cannot create order.");
            return;
        }

        try {
            // Build order payload from cart items
            const orderData = {
                items: cart.map(item => ({
                    book_id: item.id,
                    quantity: item.quantity,
                })),
            };
            // Create the order for the user. Backend route is POST /orders/{user_id}
            const response = await api.orders.createOrder(Number(userId), orderData);
            // If creation succeeded, clear cart and navigate to a thank-you page with the order
            clearCart();
            alert("Order submitted successfully.");
            navigate("/order-success", { state: { order: response.data } });
        } catch (error) {
            console.error("Error creating order:", error);
            alert("Failed to submit order. Please try again.");
        }
    };

    const total = cart.reduce((acc, item) => acc + Number(item.price) * item.quantity, 0);

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-3xl font-extrabold text-slate-800 mb-6">Shopping Cart</h1>
                {cart.length === 0 ? (
                    <p className="text-slate-600">Your cart is empty.</p>
                ) : (
                    <div>
                        <div className="flow-root">
                            <ul role="list" className="-my-6 divide-y divide-slate-200">
                                {cart.map((item) => (
                                    <li key={item.id} className="flex py-6">
                                        <div className="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-slate-200">
                                            <img
                                                src={item.cover_image_url || `https://placehold.co/300x450/cccccc/ffffff?text=Image+Not+Found`}
                                                alt={item.title}
                                                className="h-full w-full object-cover object-center"
                                            />
                                        </div>

                                        <div className="ml-4 flex flex-1 flex-col">
                                            <div>
                                                <div className="flex justify-between text-base font-medium text-slate-900">
                                                    <h3>
                                                        <a href="#">{item.title}</a>
                                                    </h3>
                                                    <p className="ml-4">€{Number(item.price).toFixed(2)}</p>
                                                </div>
                                                <p className="mt-1 text-sm text-slate-500">{item.author?.first_name} {item.author?.last_name}</p>
                                            </div>
                                            <div className="flex flex-1 items-end justify-between text-sm">
                                                <p className="text-slate-500">Qty {item.quantity}</p>
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="border-t border-slate-200 px-4 py-6 sm:px-6 mt-6">
                            <div className="flex justify-between text-base font-medium text-slate-900">
                                <p>Subtotal</p>
                                <p>€{total.toFixed(2)}</p>
                            </div>
                            <p className="mt-0.5 text-sm text-slate-500">Shipping and taxes calculated at checkout.</p>
                            <div className="mt-6">
                                <Button onClick={handleCheckout} className="w-full" disabled={!token}>Checkout</Button>
                            </div>
                            <div className="mt-4">
                                <Button onClick={clearCart} variant="outline" className="w-full">Clear Cart</Button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};
