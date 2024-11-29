from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# If you want to modify files in addition to uploading, add 'https://www.googleapis.com/auth/drive'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_google_drive_service():
    creds = None
    
    # Check if we have stored credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no credentials or if they're invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret_1022633783512-8potfj82biq43165smtkmaih1scrov4u.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)

def upload_image(image_path, folder_id=None):
    """Upload an image to Google Drive"""
    try:
        service = get_google_drive_service()
        
        # Prepare file metadata
        file_metadata = {'name': os.path.basename(image_path)}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Prepare media
        media = MediaFileUpload(
            image_path, 
            mimetype='image/*',
            resumable=True
        )
        
        # Upload file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f'Successfully uploaded {image_path}')
        print(f'File ID: {file.get("id")}')
        return file.get('id')
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None

def share_file_with_user(file_id, email):
    """Share a file with another user on Google Drive."""
    try:
        service = get_google_drive_service()
        
        # Create a permission for the other user
        permission = {
            'type': 'user',
            'role': 'writer',  # or 'reader' if you only want them to view
            'emailAddress': email
        }
        
        # Add the permission to the file
        service.permissions().create(
            fileId=file_id,
            body=permission,
            fields='id'
        ).execute()
        
        print(f'Shared file with {email}')
    except Exception as e:
        print(f'An error occurred while sharing: {str(e)}')

# Example usage
if __name__ == '__main__':
    # Define the image path and recipient email
    image_path = '/home/clement8242133/test.jpg'  # Change this to your image path
    recipient_email = 'recipient_email@example.com'  # Replace with the recipient's email

    # Upload a single image and share it
    file_id = upload_image(image_path)
    if file_id:
        share_file_with_user(file_id, recipient_email)

    # To upload to a specific folder, provide the folder ID
    # folder_id = 'your_folder_id_here'
    # file_id = upload_image(image_path, folder_id)
    # if file_id:
    #     share_file_with_user(file_id, recipient_email)

    # To upload and share all images in a directory
    image_directory = '/home/clement8242133/'  # Change this to your directory path
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            full_path = os.path.join(image_directory, filename)
            file_id = upload_image(full_path)
            if file_id:
                share_file_with_user(file_id, recipient_email)

