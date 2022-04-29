import gzip
import os
import pandas as pd
import openpyxl as excel
import glob
from definitions import ROOT_DIR
import json

path = os.path.join(ROOT_DIR, "openhumans", '23andme')

extension = 'json.gz'

os.chdir(path)

files = [i for i in glob.glob('*.{}'.format(extension))]

os.chdir(os.path.join(ROOT_DIR, "openhumans"))

print(files)
n=0
for i in files:
    n+=1
    with gzip.open(os.path.join(path, i), "r") as f:
        data = json.loads(f.read(), encoding="utf-8")
    out_file = open(i.split(".")[0]+".json", "w")
    json.dump(data, out_file)
    out_file.close()
    os.remove(os.path.join(path, i))
