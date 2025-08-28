import { type FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Home } from './components/Home';
import { About } from './components/About';
import { Login } from './components/Login';
import { Cart } from './components/Cart';
import { OurStory } from './components/OurStory';
import { Careers } from './components/Careers';
import { ContactUs } from './components/ContactUs';
import { FAQ } from './components/FAQ';
import { BookPage } from './components/BookPage';
import { Signup } from './components/Signup';
import { UserPage } from './components/UserPage';
import ThankYou from './components/ThankYou';
import OrderDetails from './components/OrderDetails';
import { CartProvider } from './context/CartContext';
import { ApiProvider } from './context/ApiContext';
import { AuthProvider } from './context/AuthContext';
import { Bestsellers } from './components/Bestsellers';



const App: FC = () => {
    return (
        <ApiProvider>
            <AuthProvider>
                <CartProvider>
                    <Router>
                        <div className="bg-slate-50 min-h-screen font-sans text-slate-800">
                            <Header />
                            <Routes>
                                <Route path="/" element={<Home />} />
                                <Route path="/bestsellers" element={<Bestsellers />} />
                                <Route path="/about" element={<About />} />
                                <Route path="/login" element={<Login />} />
                                <Route path="/cart" element={<Cart />} />
                                <Route path="/our-story" element={<OurStory />} />
                                <Route path="/careers" element={<Careers />} />
                                <Route path="/contact-us" element={<ContactUs />} />
                                <Route path="/faq" element={<FAQ />} />
                                <Route path="/books/:id" element={<BookPage />} />
                                <Route path="/signup" element={<Signup />} />
                                <Route path="/me" element={<UserPage />} />
                                <Route path="/order-success" element={<ThankYou />} />
                                <Route path="/orders/:id" element={<OrderDetails />} />
                            </Routes>
                            <Footer />
                        </div>
                    </Router>
                </CartProvider>
            </AuthProvider>
        </ApiProvider>
    );
};

export default App;