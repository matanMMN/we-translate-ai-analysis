"use client"

import IconButton from "@mui/material/IconButton";
import {openDrawer, selectDrawer} from "@/store/slices/drawerSlice";
import MenuIcon from "@mui/icons-material/Menu";
import AppLogo from "@/components/header/AppLogo";
import LanguageButton from "@/components/header/LanguageButton";
import {Toolbar} from "@mui/material";
import {AppDispatch} from "@/store/store.types";
import {useDispatch, useSelector} from "react-redux";

export default function HeaderToolBar() {

    const dispatch: AppDispatch = useDispatch();
    const isOpen = useSelector(selectDrawer)

    return (
        <Toolbar className={"flex flex-row w-full justify-between"}>
            <div className={"flex flex-row"}>
                {!isOpen &&
                    <IconButton
                        color="inherit"
                        className={`text-white`}
                        aria-label="open drawer"
                        onClick={() => dispatch(openDrawer())}
                        edge="start"
                    >
                        <MenuIcon/>
                    </IconButton>
                }
                <AppLogo/>
            </div>
            <div className="flex items-center mr-[2rem]">
                <LanguageButton/>
            </div>
        </Toolbar>
    )
}