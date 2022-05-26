import os
import mimetypes

folder_path = "/Users/nav/Desktop/aoc"


def main():

    files = os.listdir(folder_path)
    files_path = []
    mime_types = []
    for file in files:
        path = f"{folder_path}/{file}"
        mime = mimetypes.guess_type(path)
        files_path.append(path)
        mime_types.append(mime[0])

    for file, mime in zip(files_path, mime_types):
        print(file, mime)


if __name__ == "__main__":
    main()
