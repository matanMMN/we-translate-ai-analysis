import React from 'react'
import image from '@/assets/icon.png';
import {AppName} from '@/config/constants';
import Image from "next/image";
import {redirect} from "next/navigation";


const AppLogo = () => {

    return (
        <div className="flex flex-col items-center justify-center px-6 min-h-20 h-full">
            <div className="flex flex-row flex-wrap items-center text-center">
                <Image onClick={() => redirect('/')}
                       className="cursor-pointer flex select-none items-center justify-center w-10 h-10 aspect-square"
                       src={image}
                       alt='App Logo'/>
                <div className="text-2xl font-normal text-white items-center justify-center h-full ml-2.5"
                     style={{fontFamily: "Arial"}}
                >
                    {AppName}
                </div>
            </div>
        </div>
    )
}


export default AppLogo;