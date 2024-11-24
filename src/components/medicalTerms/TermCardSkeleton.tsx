import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function TermCardSkeleton() {
    return (
        <Card className="h-full min-h-[250px] transition-transform hover:-translate-y-1 hover:shadow-lg">
            <CardContent className="p-6 flex flex-col h-full">
                <div className="space-y-2">
                    <div className="flex justify-between items-center">
                        <Skeleton className="h-8 w-32" />
                        <Skeleton className="h-5 w-16" />
                    </div>
                    <Skeleton className="h-5 w-full" />
                </div>
                <div className="mt-6 flex-grow">
                    <Skeleton className="h-full w-full min-h-[100px]" />
                </div>
            </CardContent>
        </Card>
    );
} 