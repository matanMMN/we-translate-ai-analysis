'use client'

import * as React from 'react'
import {Badge} from '@/components/ui/badge'
import {Avatar, AvatarFallback, AvatarImage} from '@/components/ui/avatar'
import {Card, CardContent} from '@/components/ui/card'
import EditOrViewGrid from "@/components/editor/EditOrViewGrid";
import {getPriorityColor, getStatusColor} from "@/lib/functions";
import {useSelector} from "react-redux";
import {selectSession} from "@/store/slices/projectSlice";


export default function ProjectDetails() {

    const session = useSelector(selectSession)
    const {project, userSession} = session

    return (
        <div className="space-y-8">
            <Card>
                <CardContent className="pt-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Name</div>
                            <div className="font-medium">{project.name}</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Status</div>
                            <div className={`font-medium ${getStatusColor(project.status)}`}>{project.status}</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Priority</div>
                            <Badge variant="secondary" className={`${getPriorityColor(project.priority)}`}>
                                {project.priority}
                            </Badge>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Last Update</div>
                            <div className="font-medium">{project.updatedAt.toLocaleString("en")}</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Source Language</div>
                            <div className="font-medium">{project.sourceLanguage}</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Target Language</div>
                            <div className="font-medium">{project.destLanguage}</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Due date</div>
                            <div className="font-medium">{project.dueDate.toLocaleString("en")}</div>
                        </div>
                        <div>
                            <div className="text-sm text-muted-foreground mb-1">Start date</div>
                            <div className="font-medium">{project.createdAt.toLocaleString("en")}</div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardContent className="pt-6">
                    <h2 className="text-lg font-semibold mb-2">Description</h2>
                    <p className="text-muted-foreground">
                        {project.description}
                    </p>
                </CardContent>
            </Card>
            {userSession && <EditOrViewGrid userSession={userSession}/>}
            <div className="grid grid-cols-2 gap-8">
                <Card>
                    <CardContent className="pt-6">
                        <h2 className="text-lg font-semibold mb-4">Members</h2>
                        <div className="flex gap-4">
                            {project.members.map((member) => (
                                <div key={member.id} className="flex items-center gap-2">
                                    <Avatar>
                                        <AvatarImage src={member.avatar}/>
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
                            {project.activities.map((activity) => (
                                <div key={activity.id} className="flex items-start gap-4">
                                    <Avatar className="mt-1">
                                        <AvatarImage src={activity.user.avatar}/>
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