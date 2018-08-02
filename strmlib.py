import glob, os


source_dir = '/home/cm/Documents/cm/strmlib/processing/digital_elevation/guadaloupe/'

os.chdir(source_dir)
for file_name in glob.glob("*.bil"):
    token = file_name.split('_')
    for e in token:
        print(e)
    print('------')


