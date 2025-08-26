import type { FC, InputHTMLAttributes } from "react";

export const Input: FC<InputHTMLAttributes<HTMLInputElement>> = ({ className = '', ...props }) => {
    return (
        <input
            className={`flex h-10 w-full rounded-md border border-slate-300 bg-transparent py-2 px-3 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 ${className}`}
            {...props}
        />
    );
};