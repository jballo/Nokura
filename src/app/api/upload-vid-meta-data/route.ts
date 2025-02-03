"use server";
import { NextResponse } from "next/server";

export async function POST(request: Request){
    const body = await request.json();
    const { vid_name, vid_id, vid_uploader_id, vid_url, embedding } = body;
    console.log("Embedding in route: ", embedding);

    const apiSecret = request.headers.get("X-API-SECRET");
    const clerkToken = request.headers.get("Authorization") || "";

    if (apiSecret !== process.env.API_SECRET) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401});
    }

    try {
        const url_endpoint = new URL(process.env.UPLOAD_VID_METADATA_ENDPOINT || "http://127.0.0.1:5000/upload-vid-metadata");

        url_endpoint.searchParams.set("vid_name", vid_name);
        url_endpoint.searchParams.set("vid_id", vid_id);
        url_endpoint.searchParams.set("vid_uploader_id", vid_uploader_id);
        url_endpoint.searchParams.set("vid_url", vid_url);
        url_endpoint.searchParams.set("embedding", embedding);

        const upload_vid_metatadata_response = await fetch(url_endpoint.toString(), {
            method: "POST",
            headers: {
                "X-API-KEY": process.env.API_KEY || "",
                "Authorization": clerkToken,
            }
        });

        if(!upload_vid_metatadata_response.ok) {
            const errorText = await upload_vid_metatadata_response.text();
            console.error("API Response: ", errorText);
            throw new Error(
                `HTTP error! status: ${upload_vid_metatadata_response.status}, message: ${errorText}`
            );
        }

        const result = await upload_vid_metatadata_response.json();

        console.log("Vid metadata upload result: ", result);

        return NextResponse.json({
            success: true,
            response: result.content
        });

    } catch (error) {
        console.error("Error processing request: ", error);
        return NextResponse.json(
            { success: false, error: "Failed to upload vid metadata to db. "},
            { status: 500 }
        );
    }

}