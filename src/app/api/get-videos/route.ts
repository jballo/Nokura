"use server";

import { NextResponse } from "next/server";

export async function POST(request: Request) {

    const apiSecret = request.headers.get("X-API-SECRET");
    const clerkToken = request.headers.get("Authorization") || "";

    if (apiSecret !== process.env.API_SECRET) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401});
    }

    try {
        const url_endpoint = new URL(process.env.GET_VIDEOS_ENDPOINT || "http://127.0.0.1:5000/videos");

        const create_user_response = await fetch(url_endpoint.toString(), {
            method: "GET",
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

        console.log("Video url retrieval result: ", result);

        return NextResponse.json({
            success: true,
            response: result.content
        });

    } catch (error) {

    }
}