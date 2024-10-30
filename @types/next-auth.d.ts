import {DefaultSession} from "next-auth";
import {User} from "@/lib/userData";

declare module "next-auth" {
    interface Session {
        user: {
            userId: string;
            name: string;
            email: string;
        } & DefaultSession["user"];
        userData?: User | undefined;
        accessToken?: string
    }
}