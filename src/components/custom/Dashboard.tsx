"use client";

import { SignedIn, SignedOut, SignInButton, SignOutButton, useAuth, useUser } from "@clerk/nextjs";
import { Button } from "../ui/button";
import { useEffect, useState } from "react";
import { UploadButton } from "./uploadthing";
// import MediaThemeInstaplay from "player.style/instaplay/react";
import { FileUpload } from "../ui/file-upload";
import uploadVideo from "@/app/actions/uploadVideo";

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

interface Video {
    user_id: string,
    vid_id: string,
    vid_name: string,
    vid_uploader_id: string,
    vid_url: string
}

interface VideoProps {
    uploadVideoMetaData: (
        vid_name: string,
        vid_id: string,
        vid_uploader_id: string,
        vid_url: string,
        clerk_token: string
    ) => Promise<{ success: boolean; response?: boolean; error?: string; }>;
    getVideos: (
        clerk_token: string
    ) => Promise<{ success: boolean; response?: Video[]; error?: string; }>;
    uploadVideo: (
        file: File
    ) => Promise<{ success: boolean; response?: string; error?: string }>;
}

interface DashboardProps {
    createUser: UserProps["createUser"];
    userExists: UserProps["userExists"];
    uploadVideoMetaData: VideoProps["uploadVideoMetaData"];
    getVideos: VideoProps["getVideos"];
    uploadVideo: VideoProps["uploadVideo"];
}

export default function Dashboard({ createUser, userExists, uploadVideoMetaData, getVideos }: DashboardProps){
    const { isSignedIn, user } = useUser();
    const { getToken } = useAuth();
    const [email, setEmail] = useState<string>("");
    const [vidSrc, setVidSrc] = useState<string>("");
    const [videos, setVideos] = useState<Video[]>([]);
    const [file, setFiles] = useState<File>();

    
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

    const handleFileUpload = async (newFile: File) => {
        console.log("newFile: ", newFile);


        const formData = new FormData();
        formData.append("image", newFile);
        console.log("FormData 'image' (in Dashboard): ", formData.get("image"))

        if(!(isSignedIn && user)){
            return
        }

        // const clerkToken = await getToken({ template: "supabase" });

        const upload_vid_resp = await uploadVideo(newFile);

        console.log("upload_vid_resp: ", upload_vid_resp);

        console.log("type of upload_vid_resp: ", typeof(upload_vid_resp))

        const result = upload_vid_resp.response;

        const vid_name = result.name;
        const vid_id = result.key;
        const vid_url = result.url;
        setVidSrc(vid_url);


        await save_video_metadata(vid_name, vid_id, user.id, vid_url);

        setFiles(newFile)
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

        const retrieveUrls = async () => {
            if (isSignedIn && user ){
                const clerkToken = await getToken({ template: "supabase" });
                const urls = await getVideos(clerkToken || "");

                const url_list = urls.response;
                console.log("Url list: ", url_list);
                setVideos(url_list || []);

            }
        }

        storeUser();
        retrieveUrls();
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

        <div className="">
            <FileUpload onChange={handleFileUpload}/>
        </div>
        <div className="h-[80vh] overflow-y-scroll snap-y snap-mandatory rounded-lg bg-black">
            {(videos.length > 0) && (
                videos.map((vid: Video) => (
                    <section key={vid.vid_id} className="h-full flex justify-center items-start p-2 snap-start">
                        <video id={vid.vid_id} controls className="h-[75vh]">
                            <source src={vid.vid_url} type="video/mp4" />
                        </video>
                    </section>
                ))
            )}
        </div>

        {/* {(vidSrc.length > 0) && (
            // <Video src={vidSrc} />
                <video controls className="h-[70vh]">
                    <source src={vidSrc} type="video/mp4" />
                </video>
        )} */}
    </div>);
}