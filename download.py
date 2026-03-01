import os
import pprint
from googleapiclient.http import MediaIoBaseDownload
import io
import argparse
from auth import create_service


def find_files(service, parents):
    results = service.files().list(
    fields="nextPageToken, files(id, name)",
    q=f"'{parents}' in parents and trashed=false").execute()
    return results.get('files', [])


def download_file(service, exist_files):
    files = exist_files
    if files:
        for name, file_id in files.items():
            print(f"файл: {name}")
    else:
        print("файлов не существует")

    while True:
        choice = input("Введите имя файла для скачивания: ").strip()
        if choice in files:
            file_id = files[choice]
            request = service.files().get_media(fileId=file_id)
            filename = f'/home/mndrn/Рабочий стол/vscode/api5/downloads/{choice}'
            fh = io.FileIO(filename, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print ("Download %d%%." % int(status.progress() * 100))
        else:
            print("Такого файлы нет в папке")
        ask = input("Хотите продолжить? ").strip().lower()
        if ask != "да":
            break


def main():
    project_path = ''
    pp = pprint.PrettyPrinter(indent=4)
    parser = argparse.ArgumentParser(description="Google Drive")
    parser.add_argument("--parent", default="", help="ID папки на Google Drive")
    args = parser.parse_args()
    parents = args.parent
    if not parents:
        print("Вы не указали айди папки")

    service = create_service()
    files = find_files(service, parents)
    exist_files = {file['name']: file['id'] for file in files}

    path = os.path.join(project_path, parents)
    os.makedirs(path, exist_ok=True)
    download_file(service, exist_files)


if __name__ == "__main__":
    main()
