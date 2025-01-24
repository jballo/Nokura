"use server";



export async function userExists(user_id: string, clerk_token: string){
    try {
        const response_url = process.env.NEXT_API_URL || 'http://localhost:3000';
        console.log("Response url: ", response_url);
    
        const response = await fetch(`${response_url}/api/user-exists`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-SECRET": process.env.API_SECRET || "",
                "Authorization": `Bearer ${clerk_token}`
            },
            body: JSON.stringify({ user_id })
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
                error instanceof Error ? error.message : "Failed to check if user is in db.",
        }
    }
}