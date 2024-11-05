"use client"
import RouterLink from "@/components/drawer/RouterLink";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import React, {useCallback} from "react";
import {signOut} from "next-auth/react";
import {useState} from "react"
import {Button} from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"

export default function Logout() {

    const [open, setOpen] = useState(false)

    const handleSignOut = useCallback(async () => {
        await signOut()
        setOpen(false)
    }, [])


    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <RouterLink primary="Log out" url={""} icon={<ExitToAppIcon/>}/>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Log out</DialogTitle>
                    <DialogDescription>
                        Are you sure you want to log out of your account?
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                    <Button variant="outline" onClick={() => setOpen(false)}>
                        Cancel
                    </Button>
                    <Button variant="destructive" onClick={handleSignOut}>
                        Log out
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}