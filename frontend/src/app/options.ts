import {NextAuthOptions} from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import {encode as defaultEncode, JWTEncodeParams} from "next-auth/jwt";
import {serverUrl} from "@/lib/functions";


export const authOptions: NextAuthOptions = {
    session: {
        strategy: "jwt",
        maxAge: 30 * 24 * 60 * 60, // 30 days
        updateAge: 24 * 60 * 60, // 24 hours
    },
    providers: [
        CredentialsProvider({
            id: "credentials",
            type: "credentials",
            name: 'credentials auth',
            credentials: {
                email: {label: "Email", type: "email"},
                password: {label: "Password", type: "password"}
            },
            async authorize(credentials: Record<"email" | "password", string> | undefined) {
                try {
                    if (!credentials)
                        return null;
                    const {email, password} = credentials;

                    if (!email || !password) {// || email !== "admin" || password !== "admin") {
                        throw new Error('Invalid credentials');
                    }

                    // const res: User = await ApiClient.auth(email, password);
                    console.log(email, password, serverUrl)
                    const data = await fetch(`${serverUrl}/auth/token`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'accept': 'application/json',
                        },
                        body: new URLSearchParams({
                            grant_type: 'password',
                            username: email,
                            password: password,
                            scope: '',
                            client_id: 'string',
                            client_secret: 'string'
                        })
                    })
                    console.log(serverUrl)
                    console.log(data)
                    const res = await data.json()
                    console.log(res)
                    if (!res.access_token) {
                        throw new Error('User not found');
                    }
                    console.log("Res", res)
                    const userRes = await fetch(`${serverUrl}/users/me/`, { // default user
                        headers: {
                            'accept': 'application/json',
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${res.access_token}`
                        }
                    })
                    const user = await userRes.json()
                    console.log(user)
                    if (user.status_code !== 200)
                        throw new Error("User not found")
                    return {
                        name: (user.data.first_name + " " + user.data.last_name) || "Null Null",
                        email: user.data.email || "null@email.com",
                        userId: user.data.id,
                        accessToken: res.access_token,
                        tokenType: res.token_type,
                    } as any
                    // return {
                    //     userId: res.id,
                    //     name: res.first_name,
                    //     email: res.email,
                    // } as unknown as User;

                } catch (e) {
                    console.error(e)
                    throw new Error("Login failed");
                }
            }
        }),
    ],
    pages: {
        signIn: '/auth',
    },
    callbacks: {
        async session({session, token}) {

            if (token) {
                session.accessToken = token.access_token as string;
                session.tokenType = token.token_type as string;
                session.userId = token.userId as string
            }

            const userRes = await fetch(`${serverUrl}/users/me/`, { // default user
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token.access_token}`
                }
            });
            const user: { status_code: number, data: { first_name: string, last_name: string } } = await userRes.json();

            if (user.status_code !== 200) {
                throw new Error("User not found");
            }

            if (user.data.first_name && user.data.last_name) {
                const newName = user.data.first_name + " " + user.data.last_name
                if (session.user.name !== newName)
                    session.user.name = newName;
            }

            return session;
        }
        ,
        async jwt({token, user}) {
            if (user) {
                token.access_token = user.accessToken;
                token.token_type = user.tokenType;
                token.userId = user.userId
            }

            return token;
        }
    },
    jwt: {
        encode: async (params: JWTEncodeParams) => {
            return defaultEncode(params);
        }
    },
}

//'Authorization' = `Bearer ${accessToken}`