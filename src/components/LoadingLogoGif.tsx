import logo from "@/assets/loading_gif.gif"
import Image from "next/image";

export default function LoadingLogoGif() {


    return (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-100">
            <div className="text-center">
                <Image
                    priority
                    src={logo}
                    width={200}
                    height={200}
                    alt="Loading..."
                    className="mx-auto"
                />
                <p className="mt-4 text-lg font-semibold text-gray-700">Loading your data...</p>
            </div>
        </div>
    )

}