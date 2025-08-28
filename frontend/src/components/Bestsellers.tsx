import { type FC, useEffect, useState } from "react";
import { useApi } from "../context/ApiContext";
import type { BestSellerRead } from "../Client";
import { BookCard } from "./BookCard.tsx";

export const Bestsellers: FC = () => {
    const api = useApi();
    const [bestsellers, setBestsellers] = useState<BestSellerRead[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchBestsellers = async () => {
            try {
                const res = await api.books.getMonthlyBestsellers();
                setBestsellers(Array.isArray(res.data) ? res.data : []);
            } catch (e) {
                console.error("Error fetching bestsellers:", e);
                setError("Failed to load bestsellers. Please try again later.");
            } finally {
                setLoading(false);
            }
        };
        fetchBestsellers();
    }, [api]);

    return (
        <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <section className="mb-8">
                <h1 className="text-3xl md:text-4xl font-extrabold text-slate-900">This Month's Bestsellers</h1>
                <p className="text-slate-600 mt-2">Top-selling books for the current month</p>
            </section>

            {loading && <p>Loading bestsellers...</p>}
            {!loading && error && <p className="text-red-600">{error}</p>}

            {!loading && !error && (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                    {bestsellers.map((entry, index) => (
                        <div key={entry.book.id} className="relative">
                            <div className="absolute left-2 top-2 z-10 bg-yellow-400 text-black rounded-full w-8 h-8 flex items-center justify-center font-bold shadow">
                                {index + 1}
                            </div>
                            <BookCard book={entry.book} />
                            <div className="mt-2 text-sm text-slate-600">Units sold: {entry.units_sold}</div>
                        </div>
                    ))}
                </div>
            )}
        </main>
    );
};

export default Bestsellers;
