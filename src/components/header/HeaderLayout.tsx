"use client"

import {ReactNode} from "react";
import {useSelector} from "react-redux";
import {selectTheme} from "@/store/slices/themeSlice";
import AppHeader from "@/components/header/Header";

export default function HeaderLayout(): ReactNode {


    const theme = useSelector(selectTheme);

    return (
        <AppHeader theme={theme}/>
    )
}