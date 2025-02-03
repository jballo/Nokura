"use server";

import { NextResponse } from "next/server";


export async function POST(request: Request) {
    const apiSecret = request.headers.get("X-API-SECRET");

    if(apiSecret !== process.env.API_SECRET) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401});
    }
    
    try {
        const formData = await request.formData();

        const file = formData.get("video");
        if(!file) {
            throw new Error(`No file`);
        }

        const flaskFormData = new FormData();
        flaskFormData.append("file", file);

        console.log("formData video (in route): ", formData.get("video"));

        const url_endpoint = new URL(process.env.CREATE_VIDEO_EMBEDDING_ENDPOINT || "http://127.0.0.1:5000/create-video-embedding");

        const create_video_embedding_response = await fetch(url_endpoint.toString(), {
            method: "POST",
            headers: {
                "X-API-KEY": process.env.API_KEY || "",
            },
            body: flaskFormData
        });

        if(!create_video_embedding_response.ok) {
            const errorText = await create_video_embedding_response.text();
            console.error("API Response: ", errorText);
            throw new Error(`HTTP error! status: ${create_video_embedding_response.status}, message: ${errorText}`);
        }

        const result = await create_video_embedding_response.json();

        console.log("Create video embedding result: ", result);

        return NextResponse.json({
            success: true,
            response: result.content
        });

    } catch (error) {
        console.error("Error: ", error);
        return NextResponse.json(
            {success: false, error: "Failed to create video embedding."},
            { status: 500 }
        );
    }
}