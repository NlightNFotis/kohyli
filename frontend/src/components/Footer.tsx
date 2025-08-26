import { Link } from "react-router-dom";
import type { FC } from "react";

export const Footer: FC = () => {
    return (
        <footer className="bg-slate-900 text-white mt-16">
            <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                    <div>
                        <h3 className="text-lg font-semibold">Shop</h3>
                        <ul className="mt-4 space-y-2">
                            <li><a href="#" className="text-slate-400 hover:text-white">Bestsellers</a></li>
                            <li><a href="#" className="text-slate-400 hover:text-white">New Arrivals</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold">About Us</h3>
                        <ul className="mt-4 space-y-2">
                            <li><Link to="/our-story" className="text-slate-400 hover:text-white">Our Story</Link></li>
                            <li><Link to="/careers" className="text-slate-400 hover:text-white">Careers</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold">Customer Service</h3>
                        <ul className="mt-4 space-y-2">
                            <li><Link to="/contact-us" className="text-slate-400 hover:text-white">Contact Us</Link></li>
                            <li><Link to="/faq" className="text-slate-400 hover:text-white">FAQ</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold">Follow Us</h3>
                        {/* Social Icons would go here */}
                    </div>
                </div>
                <div className="mt-8 border-t border-slate-700 pt-6 text-center text-slate-400">
                    <p>&copy; 2025 Vivliopoleio Kohyli. All Rights Reserved.</p>
                </div>
            </div>
        </footer>
    );
};