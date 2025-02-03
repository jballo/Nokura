"use server";


export default async function createVideoEmbedding(file: File) {
    console.log("File in action createVideoEmbedding: ", file);
    try {
        const formData = new FormData();
        formData.append("video", file);

        const url = process.env.NEXT_API_URL || 'http://localhost:3000';

        const response = await fetch(`${url}/api/create-video-embedding`, {
            method: "POST",
            headers: {
                "X-API-SECRET": process.env.API_SECRET || ""
            },
            body: formData
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
                error instanceof Error ? error.message : "Failed to create video embedding.",
        }
    }
}