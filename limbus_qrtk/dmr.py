# -*- coding: utf-8 -*-
# encoding: utf-8

from pylibdmtx.pylibdmtx import decode as dmtx_decode
import numpy as np
import cv2
import datetime
import matplotlib.pyplot as plt

# Copyright (c) 2019 Keiron O'Shea
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA

class DataMatrixReader:
    def __init__(self, fp: str, delta: int = 200):
        self.fp = fp
        self.delta = delta

        self._load_and_process()

        self._decode_results = dmtx_decode(self.img)

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

    def to_img(self, fp: str) -> None:
        plt.plot()
        plt.imshow(self.img)

        for result, values in self.grid.items():
            d = self.to_limbus_json()["data"][result]

            result_txt = "%s\n[%i, %i]" % (result, d["row"], d["column"])
            plt.text(values["x"], values["y"], result_txt, bbox=dict(facecolor="white"))

        plt.savefig(fp)