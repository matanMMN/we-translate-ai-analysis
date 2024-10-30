"use client"
import {selectDrawer, toggleDrawer} from "@/store/slices/drawerSlice";
import {ChildrenProps} from "@/app/(content)/layout";
import {useDispatch, useSelector} from "react-redux";
import {SidebarProvider} from "@/components/ui/sidebar";

export default function DrawerProvider({children}: ChildrenProps) {
    const isOpen = useSelector(selectDrawer)
    const dispatch = useDispatch()
    return (
        <SidebarProvider open={isOpen} onOpenChange={() => dispatch(toggleDrawer())} className="overflow-hidden">
            {children}
        </SidebarProvider>
    )
}
