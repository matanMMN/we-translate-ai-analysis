"use client"

import React, {ReactNode} from 'react';
import {Sidebar, SidebarContent, useSidebar} from "@/components/ui/sidebar";
import StaticMenu from "@/components/drawer/StaticMenu";
import UserProfilePanel from "@/components/drawer/UserProfilePanel";
import {ChevronLeft} from "lucide-react"
import MenuBar from "@/components/drawer/MenuBar";

const LeftDrawer = (): ReactNode => {

    const {toggleSidebar} = useSidebar()

    return (
        <Sidebar
            className={`fixed top-0 mt-[80px] left-0 h-full transition-all duration-300 ease-in-out`}>
            <SidebarContent className="flex flex-col h-full bg-[#F0F2F5]">
                <button className="p-4 w-full justify-end items-end content-end flex flex-row"
                        onClick={toggleSidebar}>
                    <ChevronLeft size={24}/>
                </button>
                <UserProfilePanel/>
                <div className="flex h-full flex-col justify-between">
                    <MenuBar/>
                    <StaticMenu/>
                </div>
            </SidebarContent>
        </Sidebar>
    )
};

export default LeftDrawer;


//"use client"
//
// import React, {ReactNode} from 'react';
// import {Sidebar, SidebarContent, useSidebar} from "@/components/ui/sidebar";
// import StaticMenu from "@/components/drawer/StaticMenu";
// import UserProfilePanel from "@/components/drawer/UserProfilePanel";
// import {ChevronLeft} from "lucide-react"
// import MenuBar from "@/components/drawer/MenuBar";
// import {
//     Search,
//     Plus,
//     Edit2,
//     Home,
//     Clock,
//     Book,
//     Files,
//     HelpCircle,
//     Settings,
//     LogOut,
//     ArrowUpDown,
//     ChevronUp,
//     ChevronDown
// } from 'lucide-react'
// import {Button} from '@/components/ui/button'
//
// const LeftDrawer = (): ReactNode => {
//
//     const {toggleSidebar} = useSidebar()
//
//     return (
//         // <motion.div
//         //     // initial={{x: -264}}
//         //     animate={{x: 0}}
//         //     transition={{type: "spring", damping: 20}}
//         // >
//         <Sidebar
//             className={`fixed top-0 mt-[80px] left-0 h-full transition-all duration-300 ease-in-out`}>
//
//             <SidebarContent className="flex flex-col h-full bg-[#203F3A] p-6">
//
//
//                 {/*<div className="flex flex-col items-center gap-2 mb-8">*/}
//                 {/*<UserProfilePanel/>*/}
//                 {/*<div className="w-8 h-8 rounded-full bg-emerald-500"/>*/}
//                 {/*<span className="font-semibold">Translate AI</span>*/}
//                 {/*</div>*/}
//
//                 <div className="flex flex-col gap-2 mb-8">
//                     <div className="flex flex-wrap text-center gap-2 content-center items-center mb-2">
//                         <div className="w-8 h-8 rounded-full bg-emerald-500"></div>
//                         <span className="text-sm text-white/60">Aviram Shabtay</span>
//                     </div>
//                     <Button variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
//                         <Plus className="w-4 h-4 mr-2"/>
//                         New Project
//                     </Button>
//                 </div>
//
//                 <nav className="space-y-1">
//                     <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
//                         <Home className="w-4 h-4 mr-3"/>
//                         Home
//                     </Button>
//                     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
//                         <Clock className="w-4 h-4 mr-3"/>
//                         History
//                     </Button>
//                     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
//                         <Book className="w-4 h-4 mr-3"/>
//                         Medical Terms
//                     </Button>
//                     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
//                         <Files className="w-4 h-4 mr-3"/>
//                         All Projects
//                     </Button>
//                     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
//                         <HelpCircle className="w-4 h-4 mr-3"/>
//                         Help Center
//                     </Button>
//                 </nav>
//
//                 <div className="mt-auto space-y-1">
//                     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
//                         <Settings className="w-4 h-4 mr-3"/>
//                         Settings
//                     </Button>
//                     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
//                         <LogOut className="w-4 h-4 mr-3"/>
//                         Log out
//                     </Button>
//                 </div>
//                 {/*<SidebarContent className="flex flex-col h-full bg-[#1D3B34]">*/}
//                 {/*    <button className="p-4 w-full justify-end items-end content-end flex flex-row"*/}
//                 {/*            onClick={toggleSidebar}>*/}
//                 {/*        <ChevronLeft size={24}/>*/}
//                 {/*    </button>*/}
//                 {/*    <UserProfilePanel/>*/}
//                 {/*    <div className="flex h-full flex-col justify-between">*/}
//                 {/*        <MenuBar/>*/}
//                 {/*        <StaticMenu/>*/}
//                 {/*    </div>*/}
//             </SidebarContent>
//         </Sidebar>
//         // </motion.div>
//     )
// };
//
// export default LeftDrawer;
//
//
// //<motion.div
// //         initial={{ x: -264 }}
// //         animate={{ x: 0 }}
// //         transition={{ type: "spring", damping: 20 }}
// //         className="w-64 border-r bg-[#1D3B34] text-white p-6"
// //       >
// // <div className="flex items-center gap-2 mb-8">
// //     <div className="w-8 h-8 rounded-full bg-emerald-500"/>
// //     <span className="font-semibold">Translate AI</span>
// // </div>
// //
// // <div className="flex flex-col gap-2 mb-8">
// //     <div className="text-sm text-white/60 mb-2">Aviram Shabtay</div>
// //     <Button variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
// //         <Plus className="w-4 h-4 mr-2"/>
// //         New Project
// //     </Button>
// // </div>
// //
// // <nav className="space-y-1">
// //     <Button variant="ghost" className="w-full justify-start text-white hover:bg-white/10">
// //         <Home className="w-4 h-4 mr-3"/>
// //         Home
// //     </Button>
// //     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
// //         <Clock className="w-4 h-4 mr-3"/>
// //         History
// //     </Button>
// //     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
// //         <Book className="w-4 h-4 mr-3"/>
// //         Medical Terms
// //     </Button>
// //     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
// //         <Files className="w-4 h-4 mr-3"/>
// //         All Projects
// //     </Button>
// //     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
// //         <HelpCircle className="w-4 h-4 mr-3"/>
// //         Help Center
// //     </Button>
// // </nav>
// //
// // <div className="mt-auto space-y-1">
// //     <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
// //         <Settings className="w-4 h-4 mr-3" />
// //             Settings
// //           </Button>
// //           <Button variant="ghost" className="w-full justify-start text-white/60 hover:bg-white/10">
// //             <LogOut className="w-4 h-4 mr-3" />
// //             Log out
// //           </Button>
// //         </div>
// //       </motion.div>