
import { type FC, useState } from "react";
import { Button } from "./ui/Button";
import { Input } from "./ui/Input";
import { useApi } from "../context/ApiContext";
import { useNavigate } from "react-router-dom";

export const Signup: FC = () => {
    const api = useApi();
    const navigate = useNavigate();
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null); // Clear previous errors
        try {
            const response = await api.users.createUser({ first_name: firstName, last_name: lastName, email, password });
            if (response.status === 200) {
                console.log("Signup successful:", response.data);
                navigate("/login");
            } else {
                setError("Signup failed. Please try again.");
            }
        

        } catch (err: any) {
            console.error("Signup error:", err);
            if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail[0].msg || "An unexpected error occurred.");
            } else {
                setError("An unexpected error occurred during signup.");
            }
        }
    };

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 flex justify-center items-center">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12 w-full max-w-md">
                <h1 className="text-3xl font-extrabold text-slate-800 mb-6 text-center">Sign Up</h1>
                {error && <p className="text-red-500 text-center mb-4">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label htmlFor="firstName" className="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                        <Input type="text" id="firstName" placeholder="John" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="lastName" className="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                        <Input type="text" id="lastName" placeholder="Doe" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                        <Input type="email" id="email" placeholder="you@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                    <div className="mb-6">
                        <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                        <Input type="password" id="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </div>
                    <Button type="submit" className="w-full">Sign Up</Button>
                </form>
                <p className="text-sm text-slate-600 mt-6 text-center">
                    Already have an account? <a href="#" className="font-medium text-sky-600 hover:underline">Login</a>
                </p>
            </div>
        </div>
    );
};
