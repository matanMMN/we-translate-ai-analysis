interface InfoFieldProps {
    label: string | number;
    value: string | number;
    className?: string;
    render?: (value: string) => React.ReactNode;
}

export function InfoField({value, className = '', render}: InfoFieldProps) {
    return (

            render ? (
                render(value as string)
            ) : (
                <div className={`font-medium ${className}`}>{value}</div>
            )

    );
} 