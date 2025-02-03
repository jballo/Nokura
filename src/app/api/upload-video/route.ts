"use server";

import { NextResponse } from "next/server";


export async function POST(request: Request) {

    const formData = await request.formData();

    const file = formData.get("video");
    if(!file){
        throw new Error(`No file`);
    }
    const flaskFormData = new FormData();
    flaskFormData.append("file", file);

    console.log("formData video (in route): ", formData.get("video"));

    const apiSecret = request.headers.get("X-API-SECRET");

    if (apiSecret !== process.env.API_SECRET) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401});
    }

    try {
        const url_endpoint = new URL(process.env.UPLOAD_VIDEO_ENDPOINT || "http://127.0.0.1:5000/upload-video");

        const upload_video_response = await fetch(url_endpoint.toString(), {
            method: "POST",
            headers: {
                "X-API-KEY": process.env.API_KEY || "",
            },
            body: flaskFormData
        });

        if(!upload_video_response.ok) {
            const errorText = await upload_video_response.text();
            console.error("API Response: ", errorText);
            throw new Error(
                `HTTP error! status: ${upload_video_response.status}, message: ${errorText}`
            );
        }
        const result = await upload_video_response.json();
        
        console.log("Video upload result: ", result);

        return NextResponse.json({
            success: true,
            response: result.content
        });

    } catch (error) {
        console.error("Error processing request: ", error);
        return NextResponse.json(
            {success: false, error: "Failed to upload video to uploadthing."},
            { status: 500 }
        );
    }
}