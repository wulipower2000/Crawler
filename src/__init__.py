import os
import sys

file_path = os.path.dirname(__file__)
folder_path = os.path.join(file_path, 'src')
abs_folder_path = os.path.abspath(folder_path)

sys.path.append(abs_folder_path)
