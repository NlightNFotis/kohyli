// Defines the structure for a single book object.
export interface Book {
    id: number;
    title: string;
    author: string;
    price: number;
    published: Date;
    description: string | null;
    stock_quantity: number;
    coverImage: string;
    rating: number;
    genre: string;
}