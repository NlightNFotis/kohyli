import { type FC, useState } from "react";
import { Search, User, ShoppingCart, Menu, X } from 'lucide-react';


import { Button } from "./ui/Button.tsx";
import { Input } from "./ui/Input.tsx";
import { SeashellLogo } from "./SeashellLogo.tsx";

export const Header: FC = () => {
    const [isMenuOpen, setIsMenuOpen] = useState<boolean>(false);

    return (
        <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-50">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <a href="#" className="flex items-center gap-2 text-xl font-bold text-slate-800">
                        <SeashellLogo className="h-8 w-8" />
                        Vivliopoleio Kohyli
                    </a>
                    <nav className="hidden md:flex md:space-x-8">
                        <a href="#" className="text-slate-600 hover:text-sky-600 transition-colors">Home</a>
                        <a href="#" className="text-slate-600 hover:text-sky-600 transition-colors">Bestsellers</a>
                        <a href="#" className="text-slate-600 hover:text-sky-600 transition-colors">Genres</a>
                        <a href="#" className="text-slate-600 hover:text-sky-600 transition-colors">About</a>
                    </nav>
                    <div className="flex items-center space-x-2">
                        <div className="relative hidden sm:block">
                            <Input type="text" placeholder="Search books..." className="w-48 lg:w-64 pl-10" />
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        </div>
                        <Button variant="ghost" size="sm"><User size={20} /></Button>
                        <Button variant="ghost" size="sm" className="relative">
                            <ShoppingCart size={20} />
                            <span className="absolute -top-1 -right-1 bg-orange-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">3</span>
                        </Button>
                        <div className="md:hidden">
                            <Button variant="ghost" size="sm" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                                {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
            {isMenuOpen && (
                <div className="md:hidden bg-white border-t border-slate-200">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-sky-600 hover:bg-slate-50">Home</a>
                        <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-sky-600 hover:bg-slate-50">Bestsellers</a>
                        <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-sky-600 hover:bg-slate-50">Genres</a>
                        <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-sky-600 hover:bg-slate-50">About</a>
                    </div>
                    <div className="px-4 py-3 border-t border-slate-200">
                        <div className="relative">
                            <Input type="text" placeholder="Search books..." className="w-full pl-10" />
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        </div>
                    </div>
                </div>
            )}
        </header>
    );
};