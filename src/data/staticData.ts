import avatar1 from '@/assets/user1avatar.svg'
import avatar2 from '@/assets/user2avatar.svg'


export const staticMembers = [
    {
        "id": "1",
        "name": "Aviram Shabtay",
        "avatar": avatar1.src
    },
    {
        "id": "2",
        "name": "Emma K.",
        "avatar": avatar2.src
    }
]

export const staticActivities = [
    {
        "id": "1",
        "user": staticMembers[0],
        "action": "deleted the word \"slovent\"",
        "timestamp": "2 days ago"
    },
    {
        "id": "2",
        "user": staticMembers[1],
        "action": "changed the name of the project",
        "timestamp": "3 days ago"
    },
    {
        "id": "3",
        "user": staticMembers[0],
        "action": "started the project",
        "timestamp": "4 days ago"
    }
]