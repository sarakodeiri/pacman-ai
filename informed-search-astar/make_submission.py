import zipfile
import os
import sys

if __name__ == '__main__':
    cwd = os.getcwd()
    file_name = "asg02_%s.zip" % sys.argv[1]
    zip_file = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    zip_file.write('search.py')
    zip_file.write('searchAgents.py')
    zip_file.close()
