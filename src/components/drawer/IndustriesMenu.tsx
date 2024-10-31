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

            <ListItemButton onClick={() => setIsIndustriesOpen(!isIndustriesOpen)}
                            className="flex items-center text-black border rounded-2xl my-2 hover:bg-gray-200">
                <ListItemIcon>
                    <AssignmentIcon className="mr-3"/>
                </ListItemIcon>
                <ListItemText className="text-2xl text-black" primary="Industries"/>
                {isIndustriesOpen ? <ChevronUp size={20}/> : <ChevronDown size={20}/>}
            </ListItemButton>


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