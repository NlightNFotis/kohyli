
import { type FC } from "react";
import { Button } from "./ui/Button";
import { Input } from "./ui/Input";

export const Login: FC = () => {
    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 flex justify-center items-center">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12 w-full max-w-md">
                <h1 className="text-3xl font-extrabold text-slate-800 mb-6 text-center">Login</h1>
                <form>
                    <div className="mb-4">
                        <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                        <Input type="email" id="email" placeholder="you@example.com" />
                    </div>
                    <div className="mb-6">
                        <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                        <Input type="password" id="password" placeholder="••••••••" />
                    </div>
                    <Button type="submit" className="w-full">Login</Button>
                </form>
                <p className="text-sm text-slate-600 mt-6 text-center">
                    Don't have an account? <a href="#" className="font-medium text-sky-600 hover:underline">Sign up</a>
                </p>
            </div>
        </div>
    );
};
