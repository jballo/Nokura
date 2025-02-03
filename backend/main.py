import os
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from supabase.client import ClientOptions
import requests
from PIL import Image
import imageio.v3 as iio
from io import BytesIO
from transformers import AutoImageProcessor, AutoModel
import torch
import numpy as np
import tempfile
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
# print(torch.backends.mps.is_available())  # Should return `True`

# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

api_key: str = os.getenv("API_KEY")
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
uploadthing_token: str = os.getenv("UPLOADTHING_SECRET")
# supabase: Client = create_client(url, key)


@app.route('/test')
def test():
    response_body = {
        "status": "success",
        "code": 200,
        "content": "Test request."
    }
    return make_response(jsonify(response_body), 200)

# Method to verify API key for authorization
def verify_auth_header(header_api_key):
        print("Testing authorization.")
        if (header_api_key != api_key):
            print("Unauthorized request")
            response_body = {
                 "status": "failed",
                 "code": 401,
                 "content": "Unauthorized request."
            }
            return make_response(jsonify(response_body), 401)
        else:
             print("Authorized request.")
             return None

@app.route('/create-user', methods=['POST'])
def add_user_to_db():
    # Verify the request is authenticated
    header_api_key = request.headers.get('X-API-Key')
    auth_check = verify_auth_header(header_api_key)
    if auth_check != None:
        return auth_check
    
    # Verify Clerk JWT
    # token = request.headers.get("Authorization", "").replace("Bearer ", "")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None


    # Get user info from request
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    print("user_id: ", user_id)
    print("email: ", email)

    try:
        # Initialize Supabase client with JWT in headers
        supabase = create_client(
            supabase_url=url,
            supabase_key=key,
            options=ClientOptions(
                headers={
                    "Authorization": f"Bearer {token}"
                },
                postgrest_client_timeout=10,
                schema="public",
            )
        )
        
        response = (
            supabase.table("users")
            .insert({ "email": email })
            .execute()
        )
        
        # Output the result
        if response.data:
            print('Inserted:', response.data)

        response_body = {
            "status": "success",
            "code": 200,
            "content": "Vid metadata successfully added to db."
        }

        return make_response(jsonify(response_body), 200)

    except Exception as err:
        # Improved error logging
        print(f"Supabase Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 500,
            "error": str(err)  # <- SAFER ERROR HANDLING
        }), 500)

@app.route('/user-exists', methods=['POST'])
def user_exists():
    print("API: '/user-exists'")
    #  Verify the request is authenticated
    header_api_key = request.headers.get('X-API-Key')
    auth_check = verify_auth_header(header_api_key)
    if auth_check != None:
        return auth_check
    
    # Get user info from request
    user_id = request.args.get('user_id')

    # Verify Clerk JWT
    # token = request.headers.get("Authorization", "").replace("Bearer ", "")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None


    try:
        print("")

        supabase = create_client(
            supabase_url=url,
            supabase_key=key,
            options=ClientOptions(
                headers={
                    "Authorization": f"Bearer {token}"
                },
                postgrest_client_timeout=10,
                schema="public",
            )
        )

        response = (
            supabase.table("users")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        print("Response data: ", response.data)
        # Output the result
        response_body = None
        if response.data:
            response_body = {
                "status": "success",
                "code": 200,
                "content": True
            }
        else:
            response_body = {
                "status": "success",
                "code": 200,
                "content": False
            }


        return make_response(jsonify(response_body), 200)


    except Exception as err:
        # Improved error logging
        print(f"Supabase Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 500,
            "error": str(err)  # <- SAFER ERROR HANDLING
        }), 500)


@app.route("/upload-vid-metadata", methods=["POST"])
def upload_vid_metadata():
    # Verify the request is authenticated
    header_api_key = request.headers.get('X-API-Key')
    auth_check = verify_auth_header(header_api_key)
    if auth_check != None:
        return auth_check
    
    # Verify Clerk JWT
    # token = request.headers.get("Authorization", "").replace("Bearer ", "")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None


    # Get vid metadata from request
    vid_id = request.args.get('vid_id')
    vid_name = request.args.get('vid_name')
    vid_url = request.args.get('vid_url')
    vid_uploader_id = request.args.get('vid_uploader_id')
    vid_embedding = request.args.get('embedding')

    try:
        
        supabase = create_client(
            supabase_url=url,
            supabase_key=key,
            options=ClientOptions(
                headers={
                    "Authorization": f"Bearer {token}"
                },
                postgrest_client_timeout=10,
                schema="public",
            )
        )

        response = (
            supabase.table("vids")
            .insert({ "vid_id": vid_id, "vid_name": vid_name, "vid_url": vid_url, "vid_uploader_id": vid_uploader_id, "embedding": vid_embedding })
            .execute()
        )
        # Output the result
        if response.data:
            print('Inserted:', response.data)

        response_body = {
            "status": "success",
            "code": 200,
            "content": "Vid metadata successfully added to db."
        }

        return make_response(jsonify(response_body), 200)
    except Exception as err:
        # Improved error logging
        print(f"Supabase Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 500,
            "error": str(err)  # <- SAFER ERROR HANDLING
        }), 500)

@app.route('/videos', methods=['GET'])
def videos():
    print("API: '/user-exists'")
    #  Verify the request is authenticated
    header_api_key = request.headers.get('X-API-Key')
    auth_check = verify_auth_header(header_api_key)
    if auth_check != None:
        return auth_check
    
    # Get user info from request
    user_id = request.args.get('user_id')

    # Verify Clerk JWT
    # token = request.headers.get("Authorization", "").replace("Bearer ", "")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None

    try:
        print("")
        supabase = create_client(
            supabase_url=url,
            supabase_key=key,
            options=ClientOptions(
                headers={
                    "Authorization": f"Bearer {token}"
                },
                postgrest_client_timeout=10,
                schema="public",
            )
        )

        response = (
            supabase.table("vids")
            .select("*")
            .execute()
        )
        print("Response data: ", response.data)

        response_body = {
            "status": "success",
            "code": 200,
            "content": response.data
        }

        return make_response(jsonify(response_body), 200)
    except Exception as err:
        print(f"Supabase Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 500,
            "error": str(err)
        }), 500)

@app.route('/upload-video', methods=["POST"])
def upload_video():
    
    try: 
        header_api_key = request.headers.get('X-API-Key')
        if header_api_key != api_key:
            raise ValueError("Unauthenticated! Invalid api key!")

        if 'file' not in request.files:
            raise TypeError("No file part.")

        vid = request.files['file']

        ut_prepare_url = "https://api.uploadthing.com/v7/prepareUpload"

        preparation_headers = {
            "Content-Type": "application/json",
            "x-uploadthing-api-key": uploadthing_token,
        }

        # Read file data to ensure accurate size calculation
        data = vid.read()  # Read file content into memory
        vid_size = len(data)  # Get size from actual data length
        # Reset file pointer after reading
        vid.seek(0)

        video_name = vid.filename
        video_size = vid_size
        video_content_type = vid.content_type

        preparation_body = {
            "fileName": video_name,
            "fileSize": video_size,
            "fileType": video_content_type
        }

        generate_presigned_url_response = requests.post(
            ut_prepare_url, 
            headers=preparation_headers, 
            json=(preparation_body))

        if generate_presigned_url_response.status_code != 200:
            raise Exception("Failed to generate presigned urls.")

        generate_signed_url_result = generate_presigned_url_response.json()

        presigned_url = generate_signed_url_result["url"]
        presigned_key = generate_signed_url_result["key"]

        # Reset file pointer 
        vid.seek(0)
        # read file data
        file_data = vid.read()

        # Prepare multipart/form-data payload
        files = {
            "file": (video_name, file_data, video_content_type)
        }

        # Upload to UploadThing's signed URL
        upload_file_response = requests.put(
            presigned_url,
            files=files  # Automatically sets Content-Type with boundary
        )

        if upload_file_response.status_code != 200:
            raise Exception("Failed to upload image file to presigned url.")

        upload_file_response_json = upload_file_response.json()
        # Get the url where image is viewable
        video_url = upload_file_response_json["ufsUrl"]

        # Prepare video info to be sent back
        video_info = {
            "key": presigned_key,
            "name": video_name,
            "url": video_url
        }

        response_body = {
            "status": "success",
            "code": 200,
            "content": video_info
        }

        print("Response body: ", response_body)

        return make_response(jsonify(response_body), 200)

    except ValueError as err:
        print(f"Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 401,
            "error": str(err)
        }), 401)
    except TypeError as err:
        print(f"Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 400,
            "error": str(err)
        }), 400)
    except Exception as err:
        print(f"Uploadthing Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 500,
            "error": str(err)
        }), 500)

def detect_scenes_in_memory(uploaded_file_bytes):  # Rename for clarity
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=True) as temp_file:
        # Write the BYTES (not FileStorage object) to the temp file
        temp_file.write(uploaded_file_bytes)
        temp_file.flush()

        # Use open_video instead of VideoManager
        video = open_video(temp_file.name)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=24))  # Lower threshold

        # Detect scenes
        video.seek(0)
        scene_manager.detect_scenes(video)
        scene_list = scene_manager.get_scene_list()
        
        return scene_list

@app.route('/create-video-embedding', methods=["POST"])
def create_video_embedding():
    print("\n\n\n--------- '/create-video-embedding' ----------\n\n\n")
    try:
        header_api_key = request.headers.get('X-API-KEY')
        if header_api_key != api_key:
            raise ValueError("Unauthenticated! Invalid api key!")
        
        if 'file' not in request.files:
            raise TypeError("No file part.")
        
        vid = request.files['file']
        vid.seek(0)  # Reset file pointer before reading
        data = vid.read()


        frames = iio.imread(BytesIO(data), plugin="pyav", format_hint=".mp4")
        print("len(frames)", len(frames))
        vid.seek(0)
        key_scenes = detect_scenes_in_memory(data)  # Pass bytes, not FileStorage
        
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base", use_fast=True)
        model = AutoModel.from_pretrained("facebook/dinov2-base").to(device)  

         # Accumulate embeddings
        sum_embedding = None
        num_frames = 0

        for i, (start_time, end_time) in enumerate(key_scenes):
            print(f"Scene {i+1}:")
            print(f"  Start: {start_time.get_seconds()}s (Frame {start_time.get_frames()})")
            print(f"  End:   {end_time.get_seconds()}s (Frame {end_time.get_frames()})")

            # Process every 12th frame in the scene
            for frame_idx in range(start_time.get_frames(), end_time.get_frames(), 12):
                pil_image = Image.fromarray(frames[frame_idx])
                inputs = processor(images=pil_image, return_tensors="pt").to(device)

                with torch.no_grad():  # Disable gradient tracking
                    outputs = model(**inputs)

                # Extract CLS token (first token) from last_hidden_state
                cls_embedding = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()

                # Accumulate embeddings
                if sum_embedding is None:
                    sum_embedding = cls_embedding
                else:
                    sum_embedding += cls_embedding
                num_frames += 1

        # Compute average embedding
        if num_frames > 0:
            avg_vid_embedding = (sum_embedding / num_frames).tolist()  # Convert to list for JSON
        else:
            avg_vid_embedding = None
        print("avg_vid_embedding: ", avg_vid_embedding)

        response_body = {
            "status": "success",
            "code": 200,
            "content": avg_vid_embedding
        }

        return make_response(jsonify(response_body), 200)

    except ValueError as err:
        print(f"Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 401,
            "error": str(err)
        }), 401)
    except TypeError as err:
        print(f"Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 400,
            "error": str(err)
        }), 400)
    except Exception as err:
        print(f"Error: {str(err)}")
        return make_response(jsonify({
            "status": "failure",
            "code": 500,
            "error": str(err)
        }), 500)

if __name__ == '__main__':
    app.run()
    # print(torch.backends.mps.is_available())  # Should return `True`