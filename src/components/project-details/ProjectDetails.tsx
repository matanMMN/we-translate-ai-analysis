'use client'

import * as React from 'react'
import { FileText } from 'lucide-react'
import { format } from 'date-fns'

import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Card, CardContent } from '@/components/ui/card'

interface ProjectMember {
    id: string
    name: string
    avatar?: string
}

interface ActivityItem {
    id: string
    user: ProjectMember
    action: string
    timestamp: string
}

export default function ProjectDetails() {
    const members: ProjectMember[] = React.useMemo(() => [
        { id: '1', name: 'Aviram Shabtay', avatar: '/placeholder.svg?height=32&width=32' },
        { id: '2', name: 'Emma K.', avatar: '/placeholder.svg?height=32&width=32' },
    ], [])

    const activities: ActivityItem[] = React.useMemo(() => [
        {
            id: '1',
            user: members[0],
            action: 'deleted the word "slovent"',
            timestamp: '2 days ago'
        },
        {
            id: '2',
            user: members[1],
            action: 'changed the name of the project',
            timestamp: '3 days ago'
        },
        {
            id: '3',
            user: members[0],
            action: 'started the project',
            timestamp: '4 days ago'
        },
    ], [members])

    return (
        <div className="space-y-8">
            <Card>
                <CardContent className="pt-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Name</div>
                            <div className="font-medium">Fostimon</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Status</div>
                            <div className="font-medium">In progress</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Priority</div>
                            <Badge variant="secondary" className="bg-amber-500/10 text-amber-500">
                                High
                            </Badge>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Last Update</div>
                            <div className="font-medium">June 10, 2024</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Source Language</div>
                            <div className="font-medium">Hebrew</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Target Language</div>
                            <div className="font-medium">English</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Due date</div>
                            <div className="font-medium">June 20, 2024</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Start date</div>
                            <div className="font-medium">May 1, 2024</div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardContent className="pt-6">
                    <h2 className="text-lg font-semibold mb-2">Description</h2>
                    <p className="text-muted-foreground">
                        The translation of the Fostimon medicine for injection.
                    </p>
                </CardContent>
            </Card>

            <div className="grid grid-cols-2 gap-8">
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
                                        <p className="text-sm text-muted-foreground">{activity.timestamp}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}