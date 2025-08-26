import { type FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Home } from './components/Home';
import { About } from './components/About';
import { Login } from './components/Login';
import { Cart } from './components/Cart';
import { CartProvider } from './context/CartContext';



const App: FC = () => {
    return (
        <CartProvider>
            <Router>
                <div className="bg-slate-50 min-h-screen font-sans text-slate-800">
                    <Header />
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/about" element={<About />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/cart" element={<Cart />} />
                    </Routes>
                    <Footer />
                </div>
            </Router>
        </CartProvider>
    );
};

export default App;