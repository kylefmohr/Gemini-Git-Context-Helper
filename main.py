import subprocess
import os
import json
import magic


def clone_repo(url, options):
    result = subprocess.run(["git", "clone", url, options], capture_output=True)
    return result


def compile_csv(file, git_folder):
    with open(file, 'w') as json_file:
        for root, dirs, files in os.walk(git_folder):
            for file in files:
                if '.git' in root:
                    continue
                # get file mimetype
                mime = magic.Magic(mime=True)
                try:
                    mimetype = mime.from_buffer(open(os.path.join(root, file), 'rb').read(1024))
                except Exception as e:
                    # TODO: Fix this!
                    # Magic runs out of memory on large files. So far, in my testing this (on one repo only),
                    # it only happened to text files, so this assumes the erroring files are text files,
                    # and therefore sets the mimetype to 'text' to avoid the error.
                    mimetype = 'text'
                if 'text' not in mimetype:
                    continue
                print(os.path.join(root, file))
                with open(os.path.join(root, file), 'r') as f:
                    contents = f.read()
                    json.dump({'file_path': os.path.join(root, file), 'file_contents': contents}, json_file)
    return file


if __name__ == "__main__":
    url = "https://github.com/kylefmohr/Gemini-Git-Context-Helper"
    options = "--recursive"
    git_folder = url.split('/')[-1]
    clone_repo(url, options)
    compile_csv("output.json", git_folder)
