
import { createContext, useContext, type ReactNode, type FC } from 'react';
import { Api } from '../Client';

const ApiContext = createContext<Api<unknown> | undefined>(undefined);

export const ApiProvider: FC<{children: ReactNode}> = ({ children }) => {
    const api = new Api({ baseURL: "http://127.0.0.1:8000" });

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
