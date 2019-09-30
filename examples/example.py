from limbus_qrtk import DataMatrixReader
import json

dmr = DataMatrixReader(".datamatrix_example.jpeg")
dmr.to_img("./datamatrix_prep.jpg")

with open("datamatrix_limbus.json", "w") as outfile:
    json.dump(dmr.to_limbus_json(), outfile, indent=4)