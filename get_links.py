import argparse
import pprint
from auth import create_service


def find_files(service, parents):
    results = service.files().list(
    fields="nextPageToken, files(id, name)",
    q=f"'{parents}' in parents and trashed=false").execute()
    return results.get('files', [])


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
    pp = pprint.PrettyPrinter(indent=4)
    parser = argparse.ArgumentParser(description="Google Drive")
    parser.add_argument("--parent", default="1nR8uuxZgoPQQf3STWPUegLn-meb34gxo", help="ID папки на Google Drive")
    args = parser.parse_args()
    parents = args.parent
    if not parents:
        print("Вы не указали айди папки")
    
    service = create_service()
    files = find_files(service, parents)
    create_public_link(service, files)


if __name__ == "__main__":
    main()
