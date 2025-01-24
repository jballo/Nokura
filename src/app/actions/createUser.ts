"use server";

export async function createUser(user_id: string, email: string, clerk_token: string) {
    console.log("User_id in action: ", user_id);
    console.log("Email in action: ", email);

    try {
        const response_url = process.env.NEXT_API_URL || 'http://localhost:3000';
        console.log("Response url: ", response_url);
    
        const response = await fetch(`${response_url}/api/create-user`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-SECRET": process.env.API_SECRET || "",
                "Authorization": `Bearer ${clerk_token}`
            },
            body: JSON.stringify({ user_id, email })
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
                error instanceof Error ? error.message : "Failed to create user in db",
        }
    }
}