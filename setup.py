import subprocess
from pathlib import Path
import os


if __name__ == '__main__':
    
    print("\n\n------------\nInstalling Required Libraries\n------------\n\n")
    
    print(subprocess.call("pip install openpyxl"))
    print(subprocess.call("pip install openpyxl_image_loader"))
    print(subprocess.call("pip install pathlib"))
    print(subprocess.call("pip install opencv_python"))
    print(subprocess.call("pip install Pillow"))
    print(subprocess.call("pip install matplotlib"))
    print(subprocess.call("pip install sentence_transformers"))
    print(subprocess.call("pip install scikit-learn"))
    print(subprocess.call("pip install scikit_image"))
    print(subprocess.call("pip install numpy"))
    print("\n\n------------\nChecking for old local Database Cache\n------------\n\n")
    
    currentPath = str(Path().resolve())
    database_cache = str(currentPath) + r'\database.txt'    

    if os.path.isfile(database_cache):
        print("Found previous local Database cache\nRemoving")
        os.remove(database_cache)
        if os.path.isfile(database_cache):
            print("Failed to remove file!")
        else:
            print("File successfully removed")


    else:
        print("No previous Database Cache found")

    print("\n\n------------\nSetup complete\n------------\n\n")