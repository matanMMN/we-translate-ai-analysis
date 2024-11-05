import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Activity } from "@/lib/userData";

interface ProjectActivityProps {
    activities: Activity[];
}

export default function ProjectActivity({ activities }: ProjectActivityProps) {
    return (
        <Card>
            <CardContent className="pt-6">
                <h2 className="text-lg font-semibold mb-4">Activity</h2>
                <div className="space-y-4">
                    {activities.map((activity) => (
                        <div key={activity.id} className="flex items-start gap-4">
                            <Avatar className="mt-1">
                                <AvatarImage src={activity.user.avatar} />
                                <AvatarFallback>{activity.user.name.charAt(0)}</AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                                <p>
                                    <span className="font-medium">{activity.user.name}</span>
                                    {' '}
                                    {activity.action}
                                </p>
                                <p className="text-sm text-muted-foreground">
                                    {activity.timestamp}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
} 