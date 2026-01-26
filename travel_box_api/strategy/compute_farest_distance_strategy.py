#!/bin/python3


import copy

from travel_box_api.strategy.strategy import Strategy
from travel_box_api.utils.geo_function import distance

from travel_box_api.data.log import DEBUG_UNABLE_TO_FIND_CENTROID, DEBUG_NO_CENTROID


# Compute where is the photo take the most fareway comparated to the centroid
class ComputeFarestDistanceStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "003"

    def __compute_farest_distance(self):
        for cluster_id, cluster in copy.deepcopy(self.clusters).items():
            try:
                centroid = cluster["centroid"]
            except KeyError:
                self.log(DEBUG_UNABLE_TO_FIND_CENTROID, f"Impossible de trouver le centroid dans le cluster {cluster_id}")
            max_distance = 0
            for photo in cluster["photos"].values():
                if "coord" not in photo or photo["coord"] is None:
                    self.log(DEBUG_NO_CENTROID, f"No GPS coordinate for the photo {photo["path"]}", photo_path=photo["path"])
                    continue
                photo_coord = photo["coord"]

                current_distance = distance(centroid, photo_coord)
                max_distance = max(max_distance, current_distance)
            self.clusters[cluster_id]["max_distance_km"] = max_distance

    def process(self):
        self.__compute_farest_distance()
