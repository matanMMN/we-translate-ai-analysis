"use client"

import {Card, CardContent, CardFooter, CardHeader, CardTitle} from "@/components/ui/card"
import {FolderPlus} from 'lucide-react'
import {motion} from "framer-motion"
import NewProjectButton from "@/components/home/NewProjectButton";

export default function NoProjects() {
    return (
        <motion.div
            initial={{opacity: 0, y: 20}}
            animate={{opacity: 1, y: 0}}
            transition={{duration: 0.5}}
            className="flex items-center justify-center min-h-[400px] p-4"
        >
            <Card className="w-full max-w-md">
                <CardHeader>
                    <motion.div
                        initial={{scale: 0}}
                        animate={{scale: 1}}
                        transition={{delay: 0.2, type: "spring", stiffness: 260, damping: 20}}
                        className="flex justify-center mb-4"
                    >
                        <FolderPlus className="w-16 h-16 text-primary"/>
                    </motion.div>
                    <CardTitle className="text-2xl font-bold text-center text-primary">No Projects Yet</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-center text-muted-foreground">
                        {"It looks like you haven't created any projects yet. Why not create one right away?"}
                    </p>
                </CardContent>
                <CardFooter className="flex justify-center">
                    <motion.div whileHover={{scale: 1.05}} whileTap={{scale: 0.95}}>
                        <NewProjectButton/>
                    </motion.div>
                </CardFooter>
            </Card>
        </motion.div>
    )
}