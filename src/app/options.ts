import {NextAuthOptions, Session} from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import ApiClient from "@/lib/ApiClient";
import {user, User} from "@/lib/userData";
import {encode as defaultEncode, JWTEncodeParams} from "next-auth/jwt";


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
            name: 'credentials login',
            credentials: {
                email: {label: "Email", type: "email"},
                password: {label: "Password", type: "password"}
            },
            async authorize(credentials: Record<"email" | "password", string> | undefined) {
                try {
                    if (!credentials)
                        return null;
                    const {email, password} = credentials;

                    if (!email || !password || email !== "admin" || password !== "admin") {
                        throw new Error('Invalid credentials');
                    }

                    const res: User = await ApiClient.login(email, password);

                    if (!res) {
                        throw new Error('User not found');
                    }

                    return {
                        userId: res.id,
                        name: res.first_name,
                        email: res.email,
                    } as unknown as User;

                } catch (e) {
                    throw e;
                }
            }
        }),
    ],
    pages: {
        signIn: '/login',
    },
    callbacks: {
        async session(props: { session: Session; }) {
            const {session} = props;

            session.accessToken = user.accessToken
            session.userData = {...user}

            return session;
        },
    },
    jwt: {
        encode: async (params: JWTEncodeParams) => {
            if (!params.token?.credentials)
                return defaultEncode(params);
            return defaultEncode(params)
        }
    }
}

//'Authorization' = `Bearer ${accessToken}`