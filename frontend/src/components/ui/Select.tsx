import React, { type FC, type ReactNode, useEffect, useRef, useState } from "react";
import { ChevronDown } from 'lucide-react';

interface SelectProps {
    value: string;
    onValueChange: (value: string) => void;
    children: ReactNode;
}

export const Select: FC<SelectProps> = ({ value, onValueChange, children }) => {
    const [isOpen, setIsOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (ref.current && !ref.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [ref]);

    const handleSelect = (val: string) => {
        onValueChange(val);
        setIsOpen(false);
    }

    return (
        <div className="relative" ref={ref}>
            <button onClick={() => setIsOpen(!isOpen)} className="flex h-10 w-full items-center justify-between rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm">
                {value}
                <ChevronDown className={`h-4 w-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>
            {isOpen && (
                <div className="absolute z-10 mt-1 w-full rounded-md border bg-white shadow-lg">
                    <div className="p-1">
                        {React.Children.map(children, (child) =>
                            React.isValidElement<{ value: string, onClick?: () => void }>(child) ? React.cloneElement(child, { onClick: () => handleSelect(child.props.value) }) : child
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

interface SelectItemProps {
    children: ReactNode;
    value: string;
    onClick?: () => void;
}

export const SelectItem: FC<SelectItemProps> = ({ children, onClick }) => (
    <div onClick={onClick} className="relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none hover:bg-slate-100">
        {children}
    </div>
);