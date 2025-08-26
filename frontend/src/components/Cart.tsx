
import { type FC } from "react";
import { useCart } from "../context/CartContext";
import { Button } from "./ui/Button";
import { useNavigate } from "react-router-dom";

export const Cart: FC = () => {
    const { cart, clearCart } = useCart();
    const navigate = useNavigate();

    const handleCheckout = () => {
        // For now, we'll just navigate to the login page.
        // In a real app, you'd check if the user is logged in first.
        navigate("/login");
    };

    const total = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);

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
                                                src={item.coverImage}
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
                                                    <p className="ml-4">${item.price.toFixed(2)}</p>
                                                </div>
                                                <p className="mt-1 text-sm text-slate-500">{item.author}</p>
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
                                <p>${total.toFixed(2)}</p>
                            </div>
                            <p className="mt-0.5 text-sm text-slate-500">Shipping and taxes calculated at checkout.</p>
                            <div className="mt-6">
                                <Button onClick={handleCheckout} className="w-full">Checkout</Button>
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
