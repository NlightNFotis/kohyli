
import { type FC, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import type { BookRead } from "../types";
import { useApi } from "../context/ApiContext";
import { Button } from "./ui/Button";
import { useCart } from "../context/CartContext";

export const BookPage: FC = () => {
    const { id } = useParams<{ id: string }>();
    const api = useApi();
    const { addToCart } = useCart();
    const [book, setBook] = useState<BookRead | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchBook = async () => {
            if (!id) return;
            try {
                const response = await api.books.getBook(parseInt(id, 10));
                setBook(response.data);
            } catch (error) {
                console.error("Error fetching book:", error);
            }
            setLoading(false);
        };

        fetchBook();
    }, [id, api]);

    if (loading) {
        return <p>Loading book...</p>;
    }

    if (!book) {
        return <p>Book not found.</p>;
    }

    const inStock = typeof book.stock_quantity === "number" ? book.stock_quantity : 0;
    const outOfStock = inStock <= 0;

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                    <img
                        src={book.cover_image_url || `https://placehold.co/300x450/cccccc/ffffff?text=Image+Not+Found`}
                        alt={`Cover of ${book.title}`}
                        className="w-full h-auto object-cover rounded-lg shadow-lg"
                    />
                </div>
                <div>
                    <h1 className="text-4xl font-extrabold text-slate-800 mb-2">{book.title}</h1>
                    <p className="text-xl text-slate-600 mb-4">{book.author?.first_name} {book.author?.last_name}</p>
                    <p className="text-3xl font-bold text-slate-800 mb-2">€{Number(book.price).toFixed(2)}</p>
                    <p className={`text-sm mb-4 ${outOfStock ? "text-red-600" : "text-slate-600"}`}>
                        {outOfStock ? "Out of stock" : `In stock: ${inStock} item${inStock === 1 ? "" : "s"}`}
                    </p>
                    <p className="text-slate-600 mb-6">{book.description}</p>
                    <div className="flex items-center space-x-4">
                        <Button onClick={() => addToCart(book)} disabled={outOfStock}>
                            {outOfStock ? "Unavailable" : "Add to Cart"}
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};
