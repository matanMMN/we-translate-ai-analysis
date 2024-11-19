"use client"
import {Button} from "@/components/ui/button";
import {Plus} from "lucide-react";
import {motion} from "framer-motion";
import Link from "next/link";

export default function NewProjectButton() {
    return (
        <motion.div
            initial={{y: 20, opacity: 0}}
            animate={{y: 0, opacity: 1}}
            transition={{delay: 0.3}}
            className="flex justify-center mb-6"
        >
            <Link href={"/new-project"}>
                <Button className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white">
                    <Plus className="w-4 h-4 mr-2"/>
                    New Project
                </Button>
            </Link>
        </motion.div>
    )
}