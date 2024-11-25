"use client"

import il from "@/assets/IL-flag.svg";
import us from "@/assets/US-flag.svg";
import {ClientLanguages} from '@/context/LanguageContext';
import Image from "next/image";
import {useDispatch, useSelector} from "react-redux";
import {changeLanguage, selectLanguage} from "@/store/slices/clientLanguageSlice";
import {AppDispatch} from "@/store/store.types";

const LanguageButton = () => {

    const language = useSelector(selectLanguage);
    const dispatch: AppDispatch = useDispatch()

    //
    // useEffect(() => {
    //     const fetchLanguage = async () => {
    //         dispatch(readLanguageWithStorage());
    //     }
    //     fetchLanguage();
    // }, [dispatch])


    return (
        <div
            className="flex items-center w-[34px] h-[34px] overflow-hidden select-none bg-black border rounded-[2rem] border-solid border-black">
            {language === ClientLanguages.HEBREW ? (
                <Image
                    className="h-[2rem] w-[2rem] cursor-pointer select-none hover:transform hover:scale-110 active:opacity-90 object-cover"
                    onClick={() => dispatch(changeLanguage(ClientLanguages.ENGLISH))}
                    alt="Hebrew"
                    src={il}
                />
            ) : (
                <Image
                    className="h-[2rem] w-[2rem] cursor-pointer select-none hover:transform hover:scale-110 active:opacity-90 object-cover"
                    onClick={() => dispatch(changeLanguage(ClientLanguages.HEBREW))}
                    alt="English"
                    src={us}
                />
            )}
        </div>
    )
}

export default LanguageButton;