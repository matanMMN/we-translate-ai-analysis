import {NextAuthOptions} from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import {encode as defaultEncode, JWTEncodeParams} from "next-auth/jwt";
import { serverUrl } from "@/lib/functions";
import { UserRole } from "@/types/roles";


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
                if (!credentials || !credentials?.email || !credentials?.password) {
                    throw new Error('Missing credentials');
                }
                try {
                    const {email, password} = credentials;
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

                    const res = await data.json()

                    if (!res || !res.access_token) {
                        throw new Error('User not found');
                    }

                    const userRes = await fetch(`${serverUrl}/users/me/`, { 
                        headers: {
                            'accept': 'application/json',
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${res.access_token}`
                        }
                    })

                    const user = await userRes.json()

                    if (user.status_code !== 200)
                        throw new Error("User not found")
                    return {
                        name: (user.data.first_name + " " + user.data.last_name) || user.data.email,
                        email: user.data.email,
                        userId: user.data.id,
                        accessToken: res.access_token,
                        tokenType: res.token_type,
                        role: user.data.role as UserRole
                    } as any

                    
                } catch (e) {
                    console.error(e)
                    throw e
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
                session.user.role = token.role as UserRole;

            }

            const userRes = await fetch(`${serverUrl}/users/me/`, {
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token.access_token}`
                }
            });

            const user = await userRes.json();

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
                token.role = user.role;
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
