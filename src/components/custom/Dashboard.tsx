"use client";

import { SignedIn, SignedOut, SignInButton, SignOutButton, useAuth, useUser } from "@clerk/nextjs";
import { Button } from "../ui/button";
import { useEffect, useState } from "react";

interface UserProps {
    createUser: (
        user_id: string,
        email: string,
        clerkToken: string
    ) => Promise<{ success: boolean; response?: string; error?: string; }>;
    userExists: (
        user_id: string,
        clerk_token: string
    ) => Promise<{ success: boolean; response?: boolean; error?: string; }>;
}

interface DashboardProps {
    createUser: UserProps["createUser"];
    userExists: UserProps["userExists"];
}

export default function Dashboard({ createUser, userExists }: DashboardProps){
    const { isSignedIn, user } = useUser();
    const { getToken } = useAuth();
    const [email, setEmail] = useState<string>("");
    
    
    
    useEffect( () => {

        const storeUser = async () => {
            if (isSignedIn && user ){
                const clerkToken = await getToken({ template: "supabase" });
                const user_in_db = (await userExists(user.id, clerkToken || "")).response;
                console.log("User in db: ", user_in_db);
                if(!user_in_db){
                    createUser(user.id, user.primaryEmailAddress?.emailAddress || "", clerkToken || "");
                }
            }
        }

        storeUser();
    }, [isSignedIn, user]);


    return(<div>
        {(email.length > 0) && (<p>
            {email}
        </p>)}
        <Button>Hello</Button>
        <SignedIn>
            <SignOutButton>
                <Button>Sign Out</Button>
            </SignOutButton>
        </SignedIn>
        <SignedOut>
            <SignInButton>
                <Button>Sign In</Button>
            </SignInButton>
        </SignedOut>
    </div>);
}