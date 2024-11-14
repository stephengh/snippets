import hou
import gzip


path = hou.pwd().evalParm("ar_ass_file")
print("Fixing meters_per_unit for %s" % (path))

# read and decompress rendered .ass.gz file
with gzip.open(path, "rb") as f:  # MUST OPEN .gz FILES IN BINARY MODE!
    fop = f.read()
    
# fix the meters_per_unit value
fop = fop.replace(b"### meters_per_unit: 1.000000", b"### meters_per_unit: 0.01")  # USE BYTES NOT STRINGS!

# write the .ass.gz file back
with gzip.open(path, "wb") as f:  # MUST OPEN .gz FILES IN BINARY MODE!
    f.write(fop)
