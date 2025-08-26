
import { createContext, useState, useContext, type ReactNode, type FC } from 'react';
import type { Book } from '../types';

interface CartItem extends Book {
    quantity: number;
}

interface CartContextType {
    cart: CartItem[];
    addToCart: (book: Book) => void;
    clearCart: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: FC<{children: ReactNode}> = ({ children }) => {
    const [cart, setCart] = useState<CartItem[]>([]);

    const addToCart = (book: Book) => {
        setCart(prevCart => {
            const existingItem = prevCart.find(item => item.id === book.id);
            if (existingItem) {
                return prevCart.map(item =>
                    item.id === book.id ? { ...item, quantity: item.quantity + 1 } : item
                );
            } else {
                return [...prevCart, { ...book, quantity: 1 }];
            }
        });
    };

    const clearCart = () => {
        setCart([]);
    };

    return (
        <CartContext.Provider value={{ cart, addToCart, clearCart }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (context === undefined) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};
