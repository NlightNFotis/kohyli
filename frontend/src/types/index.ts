export interface BookRead {
    id: number;
    title: string;
    isbn: string;
    price: string;
    published_date: string;
    description?: string | null;
    stock_quantity: number;
    cover_image_url?: string | null;
    author?: AuthorRead | null;
    genre?: string;
}

export interface AuthorRead {
    id: number;
    first_name: string;
    last_name: string;
    biography?: string | null;
}