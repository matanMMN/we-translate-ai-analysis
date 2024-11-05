import {ReactNode} from "react";
import {Theme} from "@/context/ThemeContext.interface";
import HeaderToolBar from "@/components/header/HeaderToolBar";
import {log} from "@/lib/log";

const AppHeader = ({theme}: { theme: Theme }): ReactNode => {
    log("Rendering Header");

    return (
        <header className={"fixed flex justify-between w-full duration-300 transition-all ease-out z-50"}
                style={{backgroundColor: theme.colors.mainColor}}>
            <HeaderToolBar/>
        </header>
    )
}

export default AppHeader;