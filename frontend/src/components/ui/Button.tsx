import type {ButtonHTMLAttributes, FC} from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'default' | 'destructive' | 'outline' | 'ghost';
    size?: 'default' | 'sm' | 'lg';
}

const Button: FC<ButtonProps> = ({ children, variant = 'default', size = 'default', className = '', ...props }) => {
    const baseStyles = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 disabled:opacity-50 disabled:pointer-events-none";

    const variants = {
        default: "bg-sky-600 text-white hover:bg-sky-700",
        destructive: "bg-red-500 text-white hover:bg-red-600",
        outline: "border border-slate-300 bg-transparent hover:bg-slate-100",
        ghost: "hover:bg-sky-100 hover:text-sky-800",
    };

    const sizes = {
        default: "h-10 py-2 px-4",
        sm: "h-9 px-3 rounded-md",
        lg: "h-11 px-8 rounded-md",
    };

    return (
        <button className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`} {...props}>
            {children}
        </button>
    );
};