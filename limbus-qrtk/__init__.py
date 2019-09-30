from pylibdmtx.pylibdmtx import decode
import numpy as np
import cv2
import datetime
import matplotlib.pyplot as plt

class DatamatrixReader:
    def __init__(self, fp: str, delta: int = 200):
        self.fp = fp
        self.delta = delta

        self._load_and_process()

        self._decode_results = decode(self.img)

        self.grid = self._get_grid()

    def _load_and_process(self) -> np.array:
        img = cv2.imread(self.fp)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY_INV)[1]

        self.img = img


    def _get_grid(self) -> dict:

        def __gridify(coord, delta):
            return np.round(coord / delta) * delta


        results_dict = {}

        for result in self._decode_results:
            results_dict[result.data.decode("utf-8")] = {
                "x": result.rect.left,
                "y": result.rect.top,
                "x_grid": __gridify(result.rect.left, self.delta),
                "y_grid": __gridify(result.rect.top, self.delta)
            }

        return results_dict


    def to_limbus_json(self) -> dict:

        x_labels = {x_g : count for count, x_g in enumerate(sorted(set([x["x_grid"] for x in self.grid.values()])))}
        y_labels = {y_g : count for count, y_g in enumerate(sorted(set([x["y_grid"] for x in self.grid.values()])))}

        limbus_json = {
            "date" : str(datetime.datetime.now()),
            "number_rows" : len(y_labels),
            "number_columns": len(x_labels),
            "number_items" : len(self.grid),
            "data" : {

            }
        }

        for result, values in self.grid.items():
            limbus_json["data"][result] = {
                "row" : y_labels[values["y_grid"]],
                "column" : x_labels[values["x_grid"]]
            }

        return limbus_json

    def to_pdf(self, fp):
        pass

