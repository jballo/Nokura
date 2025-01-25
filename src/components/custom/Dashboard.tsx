"use client";

import { SignedIn, SignedOut, SignInButton, SignOutButton, useAuth, useUser } from "@clerk/nextjs";
import { Button } from "../ui/button";
import { useEffect, useState } from "react";
import { UploadButton } from "./uploadthing";
import MediaThemeInstaplay from "player.style/instaplay/react";

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

interface VideoProps {
    uploadVideoMetaData: (
        vid_name: string,
        vid_id: string,
        vid_uploader_id: string,
        vid_url: string,
        clerk_token: string
    ) => Promise<{ success: boolean; response?: boolean; error?: string; }>;
}

interface DashboardProps {
    createUser: UserProps["createUser"];
    userExists: UserProps["userExists"];
    uploadVideoMetaData: VideoProps["uploadVideoMetaData"];
}

export default function Dashboard({ createUser, userExists, uploadVideoMetaData }: DashboardProps){
    const { isSignedIn, user } = useUser();
    const { getToken } = useAuth();
    const [email, setEmail] = useState<string>("");
    const [vidSrc, setVidSrc] = useState<string>("");
    
    const save_video_metadata = async (vid_name: string, vid_id: string, vid_uploader_id: string, vid_url: string) => {
        console.log("Client side 'save_video_metadata' function.");
        console.log("Vid name: ", vid_name);
        console.log("Vid id: ", vid_id);
        console.log("Vid uploader id: ", vid_uploader_id);
        console.log("Vid url: ", vid_url);

        try {
            const clerkToken = await getToken({ template: "supabase" });
            const response = await uploadVideoMetaData(vid_name, vid_id, vid_uploader_id, vid_url, clerkToken || "");
            setVidSrc(vid_url);
            console.log("vidSrc: ", vidSrc);
        } catch (err) {
            console.error("Error saving video metadata in db.");
        }
    }
    
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
        <UploadButton
            endpoint="imageUploader"
            onClientUploadComplete={async (res) => {
                // Do something with the response
                // console.log("Files: ", res);
                console.log("Res data: ", res[0]);
                // console.log("Video name: ", res[0].name);
                const vid_name = res[0].name;
                // console.log("Video id: ", res[0].key);
                const vid_id = res[0].key;
                // console.log("Video user_id: ", res[0].serverData.uploadedBy);
                const vid_uploader_id = res[0].serverData.uploadedBy;
                // console.log("Video url: ", res[0].url);
                const vid_url = res[0].url;
                alert("Upload Completed");


                await save_video_metadata(vid_name, vid_id, vid_uploader_id, vid_url);
            }}
            onUploadError={(error: Error) => {
                // Do something with the error.
                alert(`ERROR! ${error.message}`);
            }}
        />


        <div className="h-[90vh] overflow-y-scroll snap-y snap-mandatory rounded-lg bg-black">
            {/* Section 1 */}
            <section className="h-[90vh] flex justify-center items-start p-6 snap-start">
                {/* <p className="text-gray-700">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                </p> */}
                {(vidSrc.length > 0) && (
                    <video controls className="h-[75vh]">
                        <source src={vidSrc} type="video/mp4" />
                    </video>
                )}
            </section>

            {/* Section 2 */}
            <section className="h-[90vh] flex justify-center items-start p-6 snap-start">
                {/* <p className="text-gray-700">
                    Fugiat adipisci in sequi alias eum perferendis tempora placeat esse.
                </p> */}
                {(vidSrc.length > 0) && (
                    <video controls className="h-[75vh]">
                        <source src={vidSrc} type="video/mp4" />
                    </video>
                )}
            </section>

            {/* Section 3 */}
            <section className="h-[90vh] flex justify-center items-start p-6 snap-start">
                {/* <p className="text-gray-700">
                    Ducimus possimus velit sunt commodi tempora placeat esse.
                </p> */}
                {(vidSrc.length > 0) && (
                    <video controls className="h-[75vh]">
                        <source src={vidSrc} type="video/mp4" />
                    </video>
                )}
            </section>
        </div>

        {/* {(vidSrc.length > 0) && (
            // <Video src={vidSrc} />
                <video controls className="h-[70vh]">
                    <source src={vidSrc} type="video/mp4" />
                </video>
        )} */}
    </div>);
}