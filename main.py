import datetime
import os
from auth import create_service
import pprint
import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import argparse


def convert_to_rfc_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + "Z"
    return dt


def find_files(service, parents):
    results = service.files().list(
    fields="nextPageToken, files(id, name)",
    q=f"'{parents}' in parents and trashed=false").execute()
    return results.get('files', [])


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


def upload_file(service, parents, exist_files, project_path):
    file_paths = [
        f'{project_path}/Script.py',
        f'{project_path}/photo.webp',
    ]
    file_names = [
        'ggdrive.py',
        'photo.webp',
    ]
    for file_path, file_name in zip(file_paths, file_names):
        media = MediaFileUpload(file_path, resumable=True)
        if file_name in exist_files:
            service.files().update(fileId=exist_files[file_name],media_body=media).execute()
            print(f"файл {file_name} перезаписан")
        else:
            file_metadata = {
                'name': file_name,
                'parents': [parents]
            }
            r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"файл {file_metadata['name']} создан")


def download_file(service, exist_files, project_path):
    if exist_files:
        for name in exist_files:
            print(f"файл: {name}")
    else:
        print("файлов не существует")

    while True:
        choice = input("Введите имя файла для скачивания: ").strip()
        if choice in exist_files:
            file_id = exist_files[choice]
            request = service.files().get_media(fileId=file_id)
            filename = f'{project_path}/downloads/{choice}'
            fh = io.FileIO(filename, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print ("Download %d%%." % int(status.progress() * 100))
        else:
            print("Такого файл нет в папке")
        ask = input("Хотите продолжить? ").strip().lower()
        if ask != "да":
            break


def create_public_link(service, files):
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }

    if not files:
        print("Файлов в папке нет")
        return

    for file in files:
        service.permissions().create(fileId=file['id'], body=permission).execute()
        file_info = service.files().get(fileId=file['id'], fields='webViewLink').execute()
        print(f"Ссылка на файл {file['name']}:", file_info['webViewLink'])


def main():
    project_path = ''

    parser = argparse.ArgumentParser(description="Google Drive")
    parser.add_argument("--parent", default="", help="ID папки на Google Drive")
    parser.add_argument("--folder_name", default="Projects", help="Имя создаваемой папки")

    args = parser.parse_args()
    folder_name = args.folder_name
    parents = args.parent
    pp = pprint.PrettyPrinter(indent=4)
    service = create_service()
    print()
    parents = create_folder(service,folder_name, parents)
    files = find_files(service, parents)
    exist_files = {file['name']: file['id'] for file in files}
    create_public_link(service, files)

    print()
    upload_file(service, parents, exist_files, project_path)
    print()


    downloads_path = os.path.join(project_path, "downloads")
    os.makedirs(downloads_path, exist_ok=True)
    download_file(service, exist_files, project_path)


if __name__ == "__main__":
    main()
