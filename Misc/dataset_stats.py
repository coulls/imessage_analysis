#Go through directories

#Open ngram.txt

#count lengths and average per directory

import os
import sys
import numpy

lang_stats = {}
for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        if name == "ngram.txt":
            lang = os.path.basename(root)

            with open(os.path.join(root,name), 'r') as f:
                lines = f.readlines()
                f.close()

                sizes = []
                for line in lines:
                    line = line.strip()
                    sizes.append(float(len(line.decode('utf-8'))))
                lang_stats[lang] = (numpy.mean(sizes), numpy.std(sizes))
print lang_stats