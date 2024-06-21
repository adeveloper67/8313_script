import requests
from ai_asistent.openai_config import OPENAI_API_KEY, GPT_MODEL
from openai import OpenAI


class OpenAIClient:
    client = OpenAI(api_key=OPENAI_API_KEY)
    files_url = 'https://api.openai.com/v1/files'
    completions_url = 'https://api.openai.com/v1/completions'

    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
        }

    def upload_file(self, file):
        try:
            # Determine Content-Type based on file extension
            content_type = self.get_content_type(file.name)
            files = {
                'file': (file.name, file.read(), content_type),
                'purpose': (None, 'fine-tune'),  # Ensure 'purpose' is included
            }
            response = requests.post(self.files_url, headers=self.headers, files=files)
            response.raise_for_status()  # Raise an exception for bad status codes
            print(f'Uploaded file successfully. Response: {response.json()}')
            return response.json()['id']
        except requests.exceptions.RequestException as e:
            print(f'Error uploading file: {e}')
            return None

    def get_files(self):
        try:
            response = requests.get(self.files_url, headers=self.headers)
            response.raise_for_status()
            files = response.json()['data']
            print(f'Fetched files successfully. Files: {files}')
            return files
        except Exception as e:
            print(f'Error fetching files: {e}')
            return None

    def generate_video_script(self, prompt, file_ids):
        messages = [{"role": "assistant", "content": f"{prompt}"}]

        if len(file_ids) > 0:
            for idx, file_id in enumerate(file_ids):
                messages.append(
                    {"role": "assistant", "content": f"File {idx + 1}: {file_id}"}
                )

        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
        )
        print(f'Generated video script successfully. Response: {response}')
        return response

    @staticmethod
    def get_content_type(filename):
        # Map file extensions to Content-Type
        extension = filename.split('.')[-1].lower()
        content_types = {
            'pdf': 'application/pdf',
            'txt': 'text/plain',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            # Add more as needed
        }
        return content_types.get(extension, 'application/octet-stream')
