#!/bin/python3
import os
import uuid

from travel_box_api.data.log import DEBUG_PARSING_DIR
from travel_box_api.strategy.strategy import Strategy
from travel_box_api.utils.load_images import load_images_from_paths_list

DEFAULT_IMPORT_DIR_PATH = "sorted/"
IMPORTED_DIR_PATH_VAR = "TB_IMPORTED_DIR_PATH"

IMPORT_DIR_PATH = os.environ.get(IMPORTED_DIR_PATH_VAR, DEFAULT_IMPORT_DIR_PATH)


NUMBER_LOCATION = 3


# Create photo cluster by existing structured dirs
class ImportClustersFromStructuredDirsStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "020"

    def _import_from_dir(self):
        locations = {cluster["location"] for cluster in self.clusters.values() if cluster.get("location")}

        self.log(DEBUG_PARSING_DIR, f"Imported dir path : {IMPORT_DIR_PATH}", path=IMPORT_DIR_PATH)

        for root, _, files in os.walk(IMPORT_DIR_PATH, followlinks=True):
            if not files:
                continue

            location = os.path.relpath(root, IMPORT_DIR_PATH).replace(os.sep, "/")

            if location in locations:
                continue

            parts_location = location.split("/")
            if len(parts_location) < NUMBER_LOCATION:
                self.log("DEBUG_994", f"{location} is not a valid struct")
                continue

            photos = load_images_from_paths_list([os.path.join(root, filename) for filename in files])

            cluster = {
                "location": location,
                "continent": parts_location[0],
                "country": parts_location[1],
                "region": parts_location[2] if len(parts_location) > NUMBER_LOCATION else "",
                "place": parts_location[3] if len(parts_location) > NUMBER_LOCATION else parts_location[2],
                "photos": {photo.sha256: photo.to_json() for photo in photos.values()},
                "imported": True,
            }

            self.clusters[str(uuid.uuid4())] = cluster
            locations.add(location)

    def process(self):
        self._import_from_dir()
