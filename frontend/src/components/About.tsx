
import { type FC } from "react";

export const About: FC = () => {
    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 mb-4">About Vivliopoleio Kohyli</h1>
                <p className="text-lg md:text-xl text-slate-600 mb-6">Welcome to Vivliopoleio Kohyli, a cozy corner for book lovers nestled in the heart of a charming Greek village. Our name, "Kohyli," means seashell in Greek, and just like a seashell, our bookstore is a treasure waiting to be discovered.</p>
                <p className="text-lg md:text-xl text-slate-600 mb-6">We believe that every book has a story to tell, and we are passionate about helping you find the perfect book to get lost in. Whether you are looking for a classic novel, a thrilling mystery, or a heartwarming romance, we have something for everyone.</p>
                <p className="text-lg md:text-xl text-slate-600 mb-6">Come and browse our shelves, enjoy a cup of traditional Greek coffee, and let us help you find your next great read. We can't wait to welcome you to our little bookstore by the sea.</p>
            </div>
        </div>
    );
};
