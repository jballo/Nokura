"use server";

export default async function getVideos(clerk_token: string){
    try {
        const response_url = process.env.NEXT_API_URL || 'http://localhost:3000';

        const response = await fetch(`${response_url}/api/get-videos`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-SECRET": process.env.API_SECRET || "",
                "Authorization": `Bearer ${clerk_token}`
            }
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
                error instanceof Error ? error.message : "Failed to get urls from db.",
        }
    }
}
