import type {FC, ReactNode} from "react";

// Card components (the base for showing off books in our store).

interface CardProps {
    children: ReactNode;
    className?: string;
}

const Card: FC<CardProps> = ({ children, className = '' }) => (
    <div className={`rounded-lg border bg-white text-slate-800 shadow-sm ${className}`}>{children}</div>
);

const CardContent: FC<CardProps> = ({ children, className = '' }) => (
    <div className={`p-4 ${className}`}>{children}</div>
);