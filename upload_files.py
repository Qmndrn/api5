import pprint
from googleapiclient.http import MediaFileUpload
import argparse
from auth import create_service


def find_files(service, parents):
    results = service.files().list(
    fields="nextPageToken, files(id, name)",
    q=f"'{parents}' in parents and trashed=false").execute()
    return results.get('files', [])


def upload_file(service, parents, exist_files):
    files = exist_files

    file_paths = [
        '/home/mndrn/Рабочий стол/vscode/api5/Script.py',
        '/home/mndrn/Рабочий стол/vscode/api5/photo.webp',
    ]
    file_names = [
        'ggdrive.py',
        'photo.webp',
    ]

    for file_path, file_name in zip(file_paths, file_names):
        media = MediaFileUpload(file_path, resumable=True)
        if file_name in files:
            service.files().update(fileId=files[file_name],media_body=media).execute()
            print(f"файл {file_name} перезаписан")
        else:
            file_metadata = {
                'name': file_name,
                'parents': [parents]
            }
            r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"файл {file_metadata['name']} создан")


def main():
    pp = pprint.PrettyPrinter(indent=4)
    service = create_service()
    parser = argparse.ArgumentParser(description="Google Drive")
    parser.add_argument("--parent", default="1nR8uuxZgoPQQf3STWPUegLn-meb34gxo", help="ID папки на Google Drive")
    args = parser.parse_args()
    parents = args.parent
    if not parents:
        print("Вы не указали айди папки")
    files = find_files(service, parents)
    exist_files = {file['name']: file['id'] for file in files}

    upload_file(service, parents, exist_files)


if __name__ == "__main__":
    main()