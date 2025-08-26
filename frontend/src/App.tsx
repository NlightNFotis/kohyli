import {type FC, useState} from 'react'

import type {Book} from "./types";
import {mockBooks} from "./data/mockBooks.ts";
import {Header} from "./components/Header.tsx";
import {Select, SelectItem} from "./components/ui/Select.tsx";
import {BookCard} from "./components/BookCard.tsx";

import './App.css'
import {Footer} from "./components/Footer.tsx";



const App: FC = () => {
    const [books] = useState<Book[]>(mockBooks);
    const [filter, setFilter] = useState<string>('All');

    const genres: string[] = ['All', ...new Set(books.map(book => book.genre))];
    const filteredBooks: Book[] = filter === 'All' ? books : books.filter(book => book.genre === filter);

    return (
        <div className="bg-slate-50 min-h-screen font-sans text-slate-800">
            <Header />

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

                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                        {filteredBooks.map(book => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                </section>
            </main>

            <Footer />
        </div>
    );
}

export default App
