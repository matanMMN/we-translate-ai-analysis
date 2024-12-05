"use client"
import {selectDrawer, toggleDrawer} from "@/store/slices/drawerSlice";
import {useSelector} from "react-redux";
import {SidebarProvider} from "@/components/ui/sidebar";
import {ChildrenProps} from "@/app/layout";
import {useAppDispatch} from "@/hooks/useAppDispatch";
// import {useAppSelector} from "@/hooks/useAppSelector";
// import {selectPath, setPath} from "@/store/slices/sessionSlice";
// import {usePathname} from "next/navigation";
// import {useEffect} from "react";

export default function DrawerProvider({children}: ChildrenProps) {

    const isOpen = useSelector(selectDrawer)
    const dispatch = useAppDispatch()
    // const curPath = useAppSelector(selectPath)
    // const path = usePathname()
    //
    // useEffect(() => {
    //     console.log("path", path)
    //     console.log("curPath", curPath)
    //     dispatch(setPath(path))
    // }, [curPath, dispatch, path])


    return (
        <SidebarProvider open={isOpen} onOpenChange={() => dispatch(toggleDrawer())} className="overflow-hidden">
            {children}
        </SidebarProvider>
    )
}
