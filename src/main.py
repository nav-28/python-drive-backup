#!/usr/bin/env python3


import apiWrapper
import mimetypes
from googleapiclient.discovery import build


TESTDIR = "/Users/nav/Desktop/aoc"


def main():
    creds = apiWrapper.connect_to_api()
    service = build("drive", "v3", credentials=creds)
    apiWrapper.upload_folder(TESTDIR, service, None)
    # folder_dict = apiWrapper.search_folder(service, 'Important Documents')
    # mime_type = mimetypes.guess_type(TESTFILE)

    # apiWrapper.upload_file(TESTFILE, mime_type[0], folder_dict['id'], service)


if __name__ == "__main__":
    main()
