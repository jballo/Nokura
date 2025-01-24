import os
from dotenv import load_dotenv
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from supabase.client import ClientOptions


# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('API_KEY')

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
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

if __name__ == '__main__':
    app.run()