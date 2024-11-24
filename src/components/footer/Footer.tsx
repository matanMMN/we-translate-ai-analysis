"use client"

import {AppName} from "@/config/constants";
import {useDispatch, useSelector} from "react-redux";
import {AppDispatch} from "@/store/store.types";
import {selectTheme, toggleTheme} from "@/store/slices/themeSlice";
import style from "./Footer.module.css"
import {log} from "@/lib/log";
import {ReactNode} from "react";

const currentYear = new Date().getFullYear();
const footerMessage = `Copyright © ${currentYear} ${AppName}`

const Footer = (): ReactNode => {
    log("Rendering Footer");

    const theme = useSelector(selectTheme);
    const dispatch: AppDispatch = useDispatch();
    return (
        <div className={style.footer} style={{
            backgroundColor: theme.colors.mainColor,
            color: theme.colors.primaryText,
        }}>
            <div className={style.footerText}>{footerMessage}</div>
            <button onClick={() => dispatch(toggleTheme())} className="hidden">
                Toggle Theme
            </button>
        </div>
    )
}


export default Footer;