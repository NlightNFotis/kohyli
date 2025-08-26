import { type FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Home } from './components/Home';
import { About } from './components/About';



const App: FC = () => {
    return (
        <Router>
            <div className="bg-slate-50 min-h-screen font-sans text-slate-800">
                <Header />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<About />} />
                </Routes>
                <Footer />
            </div>
        </Router>
    );
};

export default App;