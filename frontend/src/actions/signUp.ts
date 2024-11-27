"use server"

import {serverUrl} from "@/lib/functions";

export const signUp = async (data: { name: string; email: string; password: string; confirmPassword: string; }) => {
    const {name, email, password} = data
    const [first_name, last_name] = name.split(' ');
    const res = await fetch(`${serverUrl}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email,
            username: email,
            password,
            first_name: first_name ?? '',
            last_name: last_name ?? ''
        })
    });
    const user = await res.json();
    console.log(user)
    const {status_code: code} = user
    if (code === 201)
        return {success: true, user}
    else if (code === 409)
        return {success: false, error: "User already exists"}
    else if (code === 400)
        return {success: false, error: "Invalid data"}
    else
        return {success: false, error: "There is an error on our side, please try again later"}
}