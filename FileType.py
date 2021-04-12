import os


FILE_TYPE = {
    '.avi': 'video',
    '.mkv': 'video',
    '.mp4': 'video',
    '.jpg': 'image',
    '.png': 'image'
}


def file_type(file_name):
    name, ext = os.path.splitext(file_name)
    if ext in FILE_TYPE:
        return FILE_TYPE[ext]
    else:
        return ''

