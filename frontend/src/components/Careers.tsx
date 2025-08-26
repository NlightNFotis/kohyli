
import { type FC } from "react";

export const Careers: FC = () => {
    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 mb-4">Careers</h1>
                <p className="text-lg md:text-xl text-slate-600 mb-6">Join our team and help us share the magic of reading with the world. We are always looking for passionate, book-loving individuals to join our team.</p>
                <div className="space-y-8">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Bookseller</h2>
                        <p className="text-slate-600 mt-2">We are looking for a friendly and knowledgeable bookseller to help our customers find their next great read. The ideal candidate will have a passion for books and a knack for customer service.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Barista</h2>
                        <p className="text-slate-600 mt-2">Do you love coffee as much as you love books? We are looking for a skilled barista to join our team and help us create a warm and welcoming atmosphere for our customers.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Storyteller</h2>
                        <p className="text-slate-600 mt-2">We are looking for an enthusiastic storyteller to host our weekly children's story time. The ideal candidate will have a love of children's literature and a talent for bringing stories to life.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
