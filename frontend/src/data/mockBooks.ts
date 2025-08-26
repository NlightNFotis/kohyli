import type { Book } from '../types';

export const mockBooks: Book[] = [
    {
        id: 1,
        title: "The Midnight Library",
        author: "Matt Haig",
        price: 15.99,
        published: new Date("2020-09-29"),
        description: "A thought-provoking novel about life's endless possibilities.",
        stock_quantity: 120,
        coverImage: "https://placehold.co/300x450/0ea5e9/ffffff?text=The+Midnight+Library",
        rating: 4.5,
        genre: "Fiction"
    },
    {
        id: 2,
        title: "Atomic Habits",
        author: "James Clear",
        price: 19.99,
        published: new Date("2018-10-16"),
        description: "An essential guide to building better habits.",
        stock_quantity: 200,
        coverImage: "https://placehold.co/300x450/38bdf8/ffffff?text=Atomic+Habits",
        rating: 4.8,
        genre: "Self-Help"
    },
    {
        id: 3,
        title: "Project Hail Mary",
        author: "Andy Weir",
        price: 18.50,
        published: new Date("2021-05-04"),
        description: "A lone astronaut's fight to save Earth from disaster.",
        stock_quantity: 75,
        coverImage: "https://placehold.co/300x450/0ea5e9/ffffff?text=Project+Hail+Mary",
        rating: 4.7,
        genre: "Sci-Fi"
    },
    {
        id: 4,
        title: "The Four Winds",
        author: "Kristin Hannah",
        price: 22.00,
        published: new Date("2021-02-02"),
        description: "A powerful story of love and resilience during the Great Depression.",
        stock_quantity: 40,
        coverImage: "https://placehold.co/300x450/38bdf8/ffffff?text=The+Four+Winds",
        rating: 4.6,
        genre: "Historical Fiction"
    },
    {
        id: 5,
        title: "Klara and the Sun",
        author: "Kazuo Ishiguro",
        price: 16.75,
        published: new Date("2021-03-02"),
        description: "A tale of love and humanity through the eyes of an artificial companion.",
        stock_quantity: 95,
        coverImage: "https://placehold.co/300x450/0ea5e9/ffffff?text=Klara+and+the+Sun",
        rating: 4.4,
        genre: "Sci-Fi"
    },
    {
        id: 6,
        title: "Crying in H Mart",
        author: "Michelle Zauner",
        price: 14.99,
        published: new Date("2021-04-20"),
        description: "A poignant memoir on family, food, and grief.",
        stock_quantity: 150,
        coverImage: "https://placehold.co/300x450/38bdf8/ffffff?text=Crying+in+H+Mart",
        rating: 4.9,
        genre: "Memoir"
    },
    {
        id: 7,
        title: "Dune",
        author: "Frank Herbert",
        price: 12.99,
        published: new Date("1965-08-01"),
        description: "An epic science fiction saga set on the desert planet Arrakis.",
        stock_quantity: 300,
        coverImage: "https://placehold.co/300x450/0ea5e9/ffffff?text=Dune",
        rating: 4.8,
        genre: "Sci-Fi"
    },
    {
        id: 8,
        title: "Educated",
        author: "Tara Westover",
        price: 17.00,
        published: new Date("2018-02-20"),
        description: "A memoir of bravery and determination to claim education.",
        stock_quantity: 80,
        coverImage: "https://placehold.co/300x450/38bdf8/ffffff?text=Educated",
        rating: 4.7,
        genre: "Memoir"
    }
];