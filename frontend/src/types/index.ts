
export interface Book {
    id: number;
    title: string;
    author_id: number;
    isbn: string;
    price: string;
    published_date: string;
    description?: string | null;
    stock_quantity: number;
    cover_image_url?: string | null;
    author?: Author;
    rating?: number;
    genre?: string;
}

export interface Author {
    id: number;
    first_name: string;
    last_name: string;
    biography?: string | null;
}
