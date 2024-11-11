import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ProjectMember } from "@/lib/userData";

interface ProjectMembersProps {
    members: ProjectMember[];
}

export default function ProjectMembers({ members }: ProjectMembersProps) {
    return (
        <Card>
            <CardContent className="pt-6">
                <h2 className="text-lg font-semibold mb-4">Members</h2>
                <div className="flex gap-4">
                    {members.map((member) => (
                        <div key={member.id} className="flex items-center gap-2">
                            <Avatar>
                                <AvatarImage src={member.avatar} />
                                <AvatarFallback>{member.name.charAt(0)}</AvatarFallback>
                            </Avatar>
                            <span className="font-medium">{member.name}</span>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
} 