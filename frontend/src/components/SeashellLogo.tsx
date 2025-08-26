import type { FC } from "react";

interface SeashellLogoProps {
    className?: string;
}

export const SeashellLogo: FC<SeashellLogoProps> = ({ className }) => (
    <svg
        className={className}
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        stroke="currentColor"
    >
        <defs>
            <linearGradient id="shellGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#a5f3fc', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#06b6d4', stopOpacity: 1 }} />
            </linearGradient>
        </defs>
        <path
            d="M50 10 C 20 10, 10 40, 10 60 C 10 90, 40 100, 50 90 C 60 100, 90 90, 90 60 C 90 40, 80 10, 50 10 Z"
            fill="url(#shellGradient)"
            transform="rotate(-25 50 50)"
        />
        <path
            d="M50 10 C 50 30, 40 40, 30 50 M50 10 C 50 30, 60 40, 70 50 M50 10 C 50 25, 45 30, 40 35 M50 10 C 50 25, 55 30, 60 35"
            stroke="#0891b2"
            strokeWidth="2"
            strokeLinecap="round"
            transform="rotate(-25 50 50)"
        />
    </svg>
);