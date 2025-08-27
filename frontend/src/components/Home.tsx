import {type FC, useState, useEffect} from 'react'

import type {BookRead} from "../types";
import {Select, SelectItem} from "./ui/Select.tsx";
import {BookCard} from "./BookCard.tsx";
import { useApi } from '../context/ApiContext';

export const Home: FC = () => {
    const api = useApi();
    const [books, setBooks] = useState<BookRead[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [filter, setFilter] = useState<string>('All');

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const response = await api.books.getAllBooks();
                setBooks(response.data);
            } catch (error) {
                console.error("Error fetching books:", error);
            }
            setLoading(false);
        };

        fetchBooks();
    }, [api]);

    const genres: string[] = loading || !Array.isArray(books) ? [] : ['All', ...new Set(books.map(book => book.genre || ''))];
    const filteredBooks: BookRead[] = filter === 'All' ? books : (Array.isArray(books) ? books.filter(book => book.genre === filter) : []);

    return (
        <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <section className="bg-sky-600 rounded-lg text-white p-8 md:p-12 mb-12 text-center">
                <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Find Your Next Great Read</h1>
                <p className="text-lg md:text-xl max-w-3xl mx-auto text-sky-100">Explore thousands of books from bestsellers to hidden gems. Your next adventure is just a page away.</p>
            </section>

            <section>
                <div className="flex flex-col sm:flex-row justify-between items-center mb-6">
                    <h2 className="text-3xl font-bold text-slate-800">Featured Books</h2>
                    <div className="mt-4 sm:mt-0 w-48">
                        <Select value={filter} onValueChange={setFilter}>
                            {genres.map(genre => (
                                <SelectItem key={genre} value={genre}>{genre}</SelectItem>
                            ))}
                        </Select>
                    </div>
                </div>

                {loading ? (
                    <p>Loading books...</p>
                ) : (
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                        {Array.isArray(filteredBooks) && filteredBooks.map(book => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                )}
            </section>
        </main>
    );
}
