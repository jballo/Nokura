"use server";


export default async function uploadVideoMetaData(vid_name: string, vid_id: string, vid_uploader_id: string, vid_url: string, clerk_token: string) {
    console.log("Logging in action...");
    console.log("Client side 'save_video_metadata' function.");
    console.log("Vid name: ", vid_name);
    console.log("Vid id: ", vid_id);
    console.log("Vid uploader id: ", vid_uploader_id);
    console.log("Vid url: ", vid_url);

    try {
        const response_url = process.env.NEXT_API_URL || 'http://localhost:3000';
        const response = await fetch(`${response_url}/api/upload-vid-meta-data`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-SECRET": process.env.API_SECRET || "",
                "Authorization": `Bearer ${clerk_token}`
            },
            body: JSON.stringify({ vid_name, vid_id, vid_uploader_id, vid_url })
        });

        if(!response.ok) {
            throw new Error(`HTTPS error! status: ${response.status}`);
        }

        const result = response.json();

        return result;

    } catch (error) {
        console.error("Error: ", error);
        return {
            success: false,
            error:
                error instanceof Error ? error.message : "Failed to upload video metadata to db",
        }
    }
}