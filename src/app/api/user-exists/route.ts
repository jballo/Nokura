"use server";

import  { NextResponse } from "next/server";

export async function POST(request: Request) {
    const body = await request.json();
    const { user_id } = body;
    
    console.log("User_id in API route: ", user_id);

    const apiSecret = request.headers.get("X-API-SECRET");
    const clerkToken = request.headers.get("Authorization") || "";

    if (apiSecret !== process.env.API_SECRET) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401});
    }

    try {
        const url_endpoint = new URL(process.env.CREATE_USER_ENDPOINT || "http://127.0.0.1:5000/user-exists");

        url_endpoint.searchParams.set("user_id", user_id);

        const create_user_response = await fetch(url_endpoint.toString(), {
            method: "POST",
            headers: {
                "X-API-KEY": process.env.API_KEY || "",
                "Authorization": clerkToken,
            }
        });

        if(!create_user_response.ok) {
            const errorText = await create_user_response.text();
            console.error("API Response: ", errorText);
            throw new Error(
                `HTTP error! status: ${create_user_response.status}, message: ${errorText}`
            );
        }

        const result = await create_user_response.json();

        console.log("User check result: ", result);

        return NextResponse.json({
            success: true,
            response: result.content
        });

    } catch (error) {
        console.error("Error processing request: ", error);
        return NextResponse.json(
            { success: false, error: "Failed to check if user in db. "},
            { status: 500 }
        );
    }
}