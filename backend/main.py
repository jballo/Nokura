import os
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from supabase.client import ClientOptions
import requests


# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('API_KEY')

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
            .insert({ "vid_id": vid_id, "vid_name": vid_name, "vid_url": vid_url, "vid_uploader_id": vid_uploader_id })
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
    #  Verify the request is authenticated
    header_api_key = request.headers.get('X-API-Key')
    auth_check = verify_auth_header(header_api_key)
    if auth_check != None:
        return auth_check

    if 'file' not in request.files:
        return make_response(jsonify({
            "status": "error",
            "code": 400,
            "content": "No file part"
        }), 400)

    vid = request.files['file']

    print("img: ", vid)

    url = "https://api.uploadthing.com/v7/prepareUpload"

    headers = {
        "Content-Type": "application/json",
        "x-uploadthing-api-key": uploadthing_token,
    }

    # Read file data to ensure accurate size calculation
    data = vid.read()  # Read file content into memory
    file_size = len(data)  # Get size from actual data length
    # Reset file pointer after reading
    vid.seek(0)

    video_name = vid.filename
    video_size = file_size
    video_content_type = vid.content_type

    body = {
        "fileName": video_name,
        "fileSize": video_size,
        "fileType": video_content_type
    }

    generate_signed_url_response = requests.post(url, headers=headers, json=(body))

    print(generate_signed_url_response.json())

    content = generate_signed_url_response.json()
    # content_key = content["key"]
    content_url = content["url"]
    content_key = content["key"]
    # Reset file pointer and read data
    vid.seek(0)
    file_data = vid.read()

    # Prepare multipart/form-data payload
    files = {
        "file": (video_name, file_data, video_content_type)
    }

    # Upload to UploadThing's signed URL
    upload_file_response = requests.put(
        content_url,
        files=files  # Automatically sets Content-Type with boundary
    )
    print("\n\n\n----------------------------\n\n\n")
    print("upload_file_response: ", upload_file_response.json()) 
    print("\n\n\n----------------------------\n\n\n")
    
    upload_file_response_json = upload_file_response.json()
    video_url = upload_file_response_json["ufsUrl"]
    video_info = {
        "key": content_key,
        "name": video_name,
        "url": video_url
    }

    response_body = {
        "status": "success",
        "code": 200,
        "content": video_info
    }
    return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    app.run()