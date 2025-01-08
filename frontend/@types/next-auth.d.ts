import {DefaultSession} from "next-auth";
import { UserRole } from '@/types/roles';

declare module "next-auth" {
    interface Session {
        user: {
            userId: string;
            name: string;
            email: string;
            role: UserRole;
        } & DefaultSession["user"];
        userData?: User | undefined;
        accessToken?: string | undefined;
        tokenType?: string | undefined;
        userId?: string | undefined
    }

    interface User {
        name: string;
        email: string;
        tokenType: string;
        accessToken: string;
        userId?: string | undefined;
        role: UserRole;
    }
}