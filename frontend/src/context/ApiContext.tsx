
import { createContext, useContext, type ReactNode, type FC, useMemo } from 'react';
import { Api, type JWTToken } from '../Client';

const ApiContext = createContext<Api<JWTToken | null> | undefined>(undefined);

export const ApiProvider: FC<{children: ReactNode}> = ({ children }) => {
    const api = useMemo(
        () =>
            new Api<JWTToken | null>({
                baseURL: "http://127.0.0.1:8000",
                securityWorker: (token) => {
                    if (!token || !token.access_token) return;
                    return {
                        headers: {
                            Authorization: `Bearer ${token.access_token}`,
                        },
                    };
                },
            }),
        [],
    );

    return (
        <ApiContext.Provider value={api}>
            {children}
        </ApiContext.Provider>
    );
};

export const useApi = () => {
    const context = useContext(ApiContext);
    if (context === undefined) {
        throw new Error('useApi must be used within an ApiProvider');
    }
    return context;
};
