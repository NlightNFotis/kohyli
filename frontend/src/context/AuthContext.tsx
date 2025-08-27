
import { createContext, useState, useContext, type ReactNode, type FC } from 'react';
import { useApi } from './ApiContext';
import type { BodyLoginUser, JWTToken } from '../Client';

interface AuthContextType {
    token: JWTToken | null;
    login: (data: BodyLoginUser) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: FC<{children: ReactNode}> = ({ children }) => {
    const api = useApi();
    const [token, setToken] = useState<JWTToken | null>(null);

    const login = async (data: BodyLoginUser) => {
        try {
            const response = await api.users.loginUser(data);
            setToken(response.data);
        } catch (error) {
            console.error("Error logging in:", error);
        }
    };

    const logout = () => {
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
