import { type FC, useEffect, useState } from "react";
import { useApi } from "../context/ApiContext";
import type { BookRead } from "../types";
import { BookCard } from "./BookCard";

export const NewArrivals: FC = () => {
    const api = useApi();
    const [books, setBooks] = useState<BookRead[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchNewArrivals = async () => {
            try {
                const res = await api.books.getNewArrivals();
                setBooks(Array.isArray(res.data) ? (res.data as unknown as BookRead[]) : []);
            } catch (e) {
                console.error("Error fetching new arrivals:", e);
                setError("Failed to load new arrivals. Please try again later.");
            } finally {
                setLoading(false);
            }
        };
        fetchNewArrivals();
    }, [api]);

    return (
        <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <section className="mb-8">
                <h1 className="text-3xl md:text-4xl font-extrabold text-slate-900">New Arrivals</h1>
                <p className="text-slate-600 mt-2">Discover the latest books added to our store</p>
            </section>

            {loading && <p>Loading new arrivals...</p>}
            {!loading && error && <p className="text-red-600">{error}</p>}

            {!loading && !error && books.length > 0 && (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                    {books.map((book) => (
                        <BookCard key={book.id} book={book} />
                    ))}
                </div>
            )}

            {!loading && !error && books.length === 0 && (
                <p>No new Arrivals this month! Stay tuned</p>
            )}
        </main>
    );
};

export default NewArrivals;
