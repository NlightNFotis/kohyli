
import { type FC } from "react";

export const FAQ: FC = () => {
    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 mb-4">Frequently Asked Questions</h1>
                <div className="space-y-8">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Do you ship internationally?</h2>
                        <p className="text-slate-600 mt-2">Yes, we ship to most countries around the world. Shipping rates and times vary depending on your location.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">What is your return policy?</h2>
                        <p className="text-slate-600 mt-2">We accept returns within 30 days of purchase. Books must be in their original condition. Please contact us for a return authorization.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Do you host events?</h2>
                        <p className="text-slate-600 mt-2">Yes, we host a variety of events, including author signings, book clubs, and children's story time. Check out our events page for a full schedule.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Do you buy used books?</h2>
                        <p className="text-slate-600 mt-2">We do not currently buy used books, but we hope to in the future.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
