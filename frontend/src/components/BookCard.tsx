import { type FC } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent } from "./ui/Card";
import { Button } from "./ui/Button";
import type { BookRead } from "../types";
import { useCart } from "../context/CartContext.tsx";

export const BookCard: FC<{ book: BookRead }> = ({ book }) => {
    const { addToCart } = useCart();

    return (
        <Card className="overflow-hidden transform hover:-translate-y-2 transition-transform duration-300 ease-in-out group">
            <div className="relative overflow-hidden">
                <img
                    src={book.cover_image_url || `https://placehold.co/300x450/cccccc/ffffff?text=Image+Not+Found`}
                    alt={`Cover of ${book.title}`}
                    className="w-full h-auto object-cover aspect-[2/3]"
                    onError={(e) => { (e.target as HTMLImageElement).onerror = null; (e.target as HTMLImageElement).src = `https://placehold.co/300x450/cccccc/ffffff?text=Image+Not+Found`; }}
                />
                <div className="absolute inset-0 bg-black bg-opacity-60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <Button onClick={() => addToCart(book)}>Add to Cart</Button>
                </div>
            </div>
            <CardContent>
                <Link to={`/books/${book.id}`}>
                    <h3 className="font-semibold text-slate-800 truncate">{book.title}</h3>
                </Link>
                <p className="text-slate-600 text-sm mt-1">{book.author?.first_name} {book.author?.last_name}</p>
                <div className="flex justify-between items-center mt-3">
                    <p className="text-lg font-bold text-slate-800">€{Number(book.price).toFixed(2)}</p>
                </div>
            </CardContent>
        </Card>
    );
};