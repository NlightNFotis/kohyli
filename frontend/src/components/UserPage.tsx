
import { type FC, useState, useEffect } from "react";
import { useApi } from "../context/ApiContext";
import type { Order } from "../Client";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function decodeJwt<T = any>(token?: string): T | null {
    if (!token) return null;
    try {
        const parts = token.split(".");
        if (parts.length < 2) return null;
        const payload = parts[1];
        // base64url -> base64
        const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
        // atob works in browsers
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

export const UserPage: FC = () => {
    const api = useApi();
    const { token } = useAuth();
    const navigate = useNavigate();
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [firstName, setFirstName] = useState<string | null>(null);
    const [lastName, setLastName] = useState<string | null>(null);

    useEffect(() => {
        if (!token) {
            navigate("/login");
            return;
        }

        // decode name fields from JWT (support several common claim names)
        const payload = decodeJwt<Record<string, any>>(token?.access_token ?? undefined);
        if (payload) {
            const fn =
                payload.first_name ??
                payload.firstName ??
                payload.given_name ??
                payload.givenName ??
                null;
            const ln =
                payload.last_name ??
                payload.lastName ??
                payload.family_name ??
                payload.familyName ??
                null;
            setFirstName(fn);
            setLastName(ln);
        }

        const fetchOrders = async () => {
            try {
                const response = await api.users.getUserOrders();
                setOrders(response.data);
            } catch (error) {
                console.error("Error fetching orders:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, [api, token, navigate]);

    if (loading) {
        return <p>Loading orders...</p>;
    }

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-4xl font-extrabold text-slate-800 mb-6">
                    {firstName || lastName ? `Orders by ${firstName ?? ""} ${lastName ?? ""}`.trim() : "Your Orders"}
                </h1>
                {orders.length === 0 ? (
                    <p>No orders found.</p>
                ) : (
                    <ul className="space-y-4">
                        {orders.map((order) => {
                            const isCancelled = (order.status ?? "").toLowerCase() === "cancelled";
                            return (
                                <li
                                    key={order.id}
                                    role="button"
                                    tabIndex={0}
                                    onClick={() => navigate(`/orders/${order.id}`)}
                                    onKeyDown={(e) => {
                                        if (e.key === "Enter" || e.key === " ") {
                                            navigate(`/orders/${order.id}`);
                                        }
                                    }}
                                    className={`border rounded-md p-4 cursor-pointer hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-sky-500 ${isCancelled ? "opacity-70" : ""}`}
                                >
                                    <div className="flex items-center justify-between">
                                        <div className={isCancelled ? "line-through" : ""}>
                                            <p className="font-semibold">Order #{order.id}</p>
                                            <p className="text-sm text-slate-600">
                                                Placed on {new Date(order.order_date).toLocaleString()}
                                            </p>
                                        </div>
                                        <div className={`text-right ${isCancelled ? "line-through" : ""}`}>
                                            <p className="font-semibold">€{Number(order.total_price).toFixed(2)}</p>
                                            <p className="text-sm text-slate-600 capitalize">{order.status}</p>
                                        </div>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                )}
            </div>
        </div>
    );
};
