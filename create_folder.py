import argparse
import os
from auth import create_service


def parse_args():
    parser = argparse.ArgumentParser(description="Google Drive")

    parser.add_argument("--parent", default="", help="ID папки на Google Drive")
    parser.add_argument("--folder_name", default="Projects", help="Имя создаваемой папки")

    return parser.parse_args()


def create_folder(service, folder_name, parents):
    if parents:
        query = f"name='Python' and '{parents}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(fields="files(id)", q=query).execute()
        if results.get('files'):
            print("Папка Python найдена")
            return results['files'][0]['id']
        else:
            metadata = {
                "name": "Python", 
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parents]
            }
            folder = service.files().create(body=metadata, fields="id").execute()
            print("Создана папка Python в папке", folder_name)
            return folder['id']
    else:
        query = f"name='{folder_name}' and 'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(fields="files(id)", q=query).execute()
        
        if results.get('files'):
            folder_id = results['files'][0]['id']
        else:
            metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder"
            }
            folder = service.files().create(body=metadata, fields="id").execute()
            folder_id = folder['id']
            print(f"Создана папка '{folder_name}'")
        
        query_python = f"name='Python' and '{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results_python = service.files().list(fields="files(id)", q=query_python).execute()
        
        if results_python.get('files'):
            print("Папка Python уже есть")
            return results_python['files'][0]['id']
        
        metadata_python = {
            "name": "Python",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [folder_id]
        }
        python_folder = service.files().create(body=metadata_python, fields="id").execute()
        print("Создана папка Python")
        return python_folder['id']


def main():
    args= parse_args()
    parents = args.parent
    folder_name = args.folder_name
    service = create_service()
    python_id = create_folder(service, folder_name, parents)


if __name__ == "__main__":
    main()
