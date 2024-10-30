"use client";
import {Provider} from "react-redux";
import store from "@/store/store";
import {ChildrenProps} from "@/app/(content)/layout";
import {ReactNode} from "react";

export const StoreProvider = ({children}: ChildrenProps): ReactNode => {
    return (
        <Provider store={store}>
            {children}
        </Provider>
    );
}