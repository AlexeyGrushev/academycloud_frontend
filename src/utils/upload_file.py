import requests

from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.utils.config import settings


def upload_file(
    file_type,
    token,
    file: UploadedFile
) -> requests.Response:
    headers = {
        'accept': 'application/json',
        # 'Content-Type': 'multipart/form-data',
    }

    files = {
        'file_type': (None, str(file_type)),
        'file': (
            file.name,
            file.getvalue(),
            file.type
            ),
    }

    cookies = {
        "user_access": token
    }

    response = requests.post(
        f'{settings.API_URL}/api/v1/file/upload_file',
        headers=headers,
        files=files,
        cookies=cookies
    )

    return response
