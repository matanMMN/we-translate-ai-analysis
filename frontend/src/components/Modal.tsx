'use client';
import React, {useCallback, useRef, useEffect, useState, MouseEventHandler} from 'react';
import {usePathname, useRouter} from 'next/navigation';

export default function Modal({children}: Readonly<{ children: React.ReactNode }>) {

    const overlay = useRef(null);
    const wrapper = useRef(null);
    const router = useRouter();
    const path = usePathname();
    const [state] = useState(path);
    console.log(state, path)
    const onDismiss = useCallback(() => {
        router.back();
    }, [router]);

    const onClick = useCallback(
        (e: MouseEventHandler<HTMLDivElement>) => {
            if ((e as unknown as MouseEvent)?.target === overlay.current || (e as unknown as MouseEvent)?.target === wrapper.current) {
                if (onDismiss) onDismiss();
            }
        },
        [onDismiss, overlay, wrapper]
    );

    const onKeyDown = useCallback(
        (e: KeyboardEvent) => {
            if (e.key === 'Escape') onDismiss();
        },
        [onDismiss]
    );

    useEffect(() => {
        document.addEventListener('keydown', onKeyDown);
        return () => document.removeEventListener('keydown', onKeyDown);
    }, [onKeyDown]);


    if (state !== path)
        return null;

    return (
        <div
            ref={overlay}
            className="fixed z-10 left-0 right-0 top-0 bottom-0 mx-auto bg-black/60 scroll-p-0"
            onClick={onClick as unknown as MouseEventHandler<HTMLDivElement>}
        >
            <div
                className="w-full h-full flex-wrap flex justify-center content-center text-black p-6"
                ref={wrapper}
            >
                {children}
            </div>
        </div>
    );
}