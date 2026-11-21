#!/bin/python3

"""
Parse all clusters and remove the empty one
"""

import copy

from travel_box_api.strategy.strategy import Strategy


class ClearEmptyClusterStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "001"

    def __clear_empty_cluster(self):
        for cluster_id, cluster in copy.deepcopy(self.clusters).items():
            if "photos" not in cluster or not cluster["photos"]:
                del self.clusters[cluster_id]

    def process(self):
        self.__clear_empty_cluster()
