"use client"
import {openDrawer, selectDrawer} from "@/store/slices/drawerSlice";
import {MenuIcon} from 'lucide-react'
import AppLogo from "@/components/header/AppLogo";
import LanguageButton from "@/components/header/LanguageButton";
import {Toolbar} from "@mui/material";
import {AppDispatch} from "@/store/store.types";
import {useDispatch, useSelector} from "react-redux";

export default function HeaderToolBar() {

    const dispatch: AppDispatch = useDispatch();
    const isOpen = useSelector(selectDrawer)

    return (
        <Toolbar className={"flex flex-row w-full justify-between "}>
            <div className={"flex flex-row"}>
                {!isOpen &&
                    <button
                        color="inherit"
                        className={`text-white`}
                        aria-label="open drawer"
                        onClick={() => dispatch(openDrawer())}

                    >
                        <MenuIcon/>
                    </button>
                }
                <AppLogo/>
            </div>
            <div className="flex items-center mr-[2rem]">
                <LanguageButton/>
            </div>
        </Toolbar>
    )
}