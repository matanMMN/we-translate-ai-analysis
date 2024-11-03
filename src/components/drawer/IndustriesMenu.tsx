"use client"

import React, {ReactNode, useState} from "react";
import {Collapse, List, ListItemButton, ListItemIcon, ListItemText} from "@mui/material";
import Link from "next/link";
import AssignmentIcon from "@mui/icons-material/Assignment";
import {ChevronDown, ChevronUp} from "lucide-react";


const workspaces = ["Cosmetics", "Leaflets", "Medical Devices"]

export default function IndustriesMenu(): ReactNode {
    const [isIndustriesOpen, setIsIndustriesOpen] = useState(false)


    return (
        <>

            <button onClick={() => setIsIndustriesOpen(!isIndustriesOpen)}
                            className=" w-full text-start hover:border-none border-none border-b-4 hover:rounded-md rounded-md inline-flex px-2 py-1 pl-2 ring-transparent ring-0 m-0 gap-0 items-center text-black border  my-2 hover:bg-gray-200">
                <ListItemIcon>
                    <AssignmentIcon className="mr-3"/>
                </ListItemIcon>
                <ListItemText className="text-2xl text-black" primary="Industries"/>
                {isIndustriesOpen ? <ChevronUp size={20}/> : <ChevronDown size={20}/>}
            </button>


            <Collapse in={isIndustriesOpen}>
                <List component="div" disablePadding>
                    {workspaces.map(w => (
                        <Link key={w} className="no-underline text-inherit"
                              href={"/" + w.toLowerCase().replaceAll(" ", "")}>
                            <button
                                className="flex items-center justify-start w-full py-2 px-4 hover:bg-[#e0e0e0] rounded text-black"
                            >
                                <div className="flex items-center justify-center text-center">
                                    {/*<AssignmentIcon className="mr-3"/>*/}
                                    <span className="ml-6 my-2">{w}</span>
                                </div>
                            </button>
                        </Link>
                    ))}
                </List>
            </Collapse>
        </>)

    {/*{workspaces.map(w =>*/
    }
    {/*    <div key={w} className="ml-[30px]">*/
    }
    {/*        <Link className="no-underline text-inherit" href={w.toLowerCase().replaceAll(" ", "")}>*/
    }
    {/*            <ListItemButton>*/
    }
    {/*                <ListItemText primary={w}/>*/
    }
    {/*            </ListItemButton>*/
    }
    {/*        </Link>*/
    }
    {/*    </div>*/
    }
    {/*)}*/
    }

}