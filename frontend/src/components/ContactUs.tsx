
import { type FC } from "react";

export const ContactUs: FC = () => {
    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 mb-4">Contact Us</h1>
                <p className="text-lg md:text-xl text-slate-600 mb-6">We would love to hear from you! Whether you have a question about a book, a suggestion for our store, or just want to say hello, we are always happy to hear from our customers.</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Visit Us</h2>
                        <p className="text-slate-600 mt-2">123 Bookworm Lane<br />Athens, Greece 12345</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Call Us</h2>
                        <p className="text-slate-600 mt-2">+30 123 456 7890</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Email Us</h2>
                        <p className="text-slate-600 mt-2">hello@kohyli.com</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
