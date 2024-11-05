interface InfoFieldProps {
    label: string | number;
    value: string | number;
    className?: string;
    render?: (value: string) => React.ReactNode;
}

export function InfoField({ label, value, className = '', render }: InfoFieldProps) {
    return (
        <div>
            <div className="text-sm text-muted-foreground mb-1">{label}</div>
            {render ? (
                render(value as string)
            ) : (
                <div className={`font-medium ${className}`}>{value}</div>
            )}
        </div>
    );
} 