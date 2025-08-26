import  { type FC } from "react";
import { Card, CardContent } from "./ui/Card";
import { Button } from "./ui/Button";
import type { Book } from "../types";
import { StarRating } from "./StarRating.tsx";

export const BookCard: FC<{ book: Book }> = ({ book }) => {
    return (
        <Card className="overflow-hidden transform hover:-translate-y-2 transition-transform duration-300 ease-in-out group">
            <div className="relative">
                <img
                    src={book.coverImage}
                    alt={`Cover of ${book.title}`}
                    className="w-full h-auto object-cover aspect-[2/3]"
                    onError={(e) => { (e.target as HTMLImageElement).onerror = null; (e.target as HTMLImageElement).src = `https://placehold.co/300x450/cccccc/ffffff?text=Image+Not+Found`; }}
                />
                <div className="absolute inset-0 bg-black bg-opacity-60 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <Button>Add to Cart</Button>
                </div>
            </div>
            <CardContent>
                <h3 className="font-semibold text-slate-800 truncate">{book.title}</h3>
                <p className="text-slate-600 text-sm mt-1">{book.author}</p>
                <div className="flex justify-between items-center mt-3">
                    <p className="text-lg font-bold text-slate-800">${book.price}</p>
                    <StarRating rating={book.rating} />
                </div>
            </CardContent>
        </Card>
    );
};