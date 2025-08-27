
import { type FC, useState, useEffect } from "react";
import { useApi } from "../context/ApiContext";
import type { User } from "../Client";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export const UserPage: FC = () => {
    const api = useApi();
    const { token } = useAuth();
    const navigate = useNavigate();
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        if (!token) {
            navigate("/login");
            return;
        }

        const fetchUser = async () => {
            try {
                const response = await api.users.getMe();
                setUser(response.data);
            } catch (error) {
                console.error("Error fetching user:", error);
            }
            setLoading(false);
        };

        fetchUser();
    }, [api, token, navigate]);

    if (loading) {
        return <p>Loading user...</p>;
    }

    if (!user) {
        return <p>User not found.</p>;
    }

    return (
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="bg-white rounded-lg shadow-lg p-8 md:p-12">
                <h1 className="text-4xl font-extrabold text-slate-800 mb-2">{user.first_name} {user.last_name}</h1>
            </div>
        </div>
    );
};
