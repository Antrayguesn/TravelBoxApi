import copy
import os

from travel_box_api.utils.clusterization import clusterize
from travel_box_api.utils.load_images import load_images_from_dir
from travel_box_api.utils.geo_function import distance
from travel_box_api.strategy.strategy import Strategy

from travel_box_api.data.log import DEBUG_PHOTO_ALREADY_DELETED, ERROR_NO_PHOTO_PATH, DEBUG_ADD_PHOTO_IN_CLUSTER, WARNING_NO_CENTROID


ESP_KM = 4

DEFAULT_PHOTOS_DIR_PATH = "photos"
UNSORTED_PHOTOS_PATH_VAR = "TB_UNSORTED_PHOTOS_PATH"


# Create cluster of photo grouped by the location (find nearest ones)
class GroupPhotosByLocationStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "006"

    def _update_clusters_with_coord(self, path_dir: str) -> dict:
        # We find the file already sorted
        exclude_file = [item for image in self.clusters.values() for item in image["photos"]]
        data_images = load_images_from_dir(path_dir, exclude_file)

        if not data_images:
            self.log(ERROR_NO_PHOTO_PATH, f"Can't find {path_dir}", path=path_dir)
            return self.clusters

        for path, image in copy.deepcopy(data_images).items():
            # We can compute distance if image have not coord data
            for id_cluster, cluster in copy.deepcopy(self.clusters).items():
                if image.coord is None:
                    pass
                elif "centroid" in cluster and cluster["centroid"] is not None:
                    d = distance(image.coord, cluster["centroid"])
                    if d < ESP_KM:
                        self.log(DEBUG_ADD_PHOTO_IN_CLUSTER,
                                 f"Add photo {image.path} to {id_cluster}",
                                 cluster_id=id_cluster,
                                 photo_path=image.path)
                        self.clusters[id_cluster]["photos"][image.sha256] = image.to_json()
                        try:
                            del data_images[path]
                        except KeyError:
                            self.log(DEBUG_PHOTO_ALREADY_DELETED, f"The photo {path} as already been deleted from the photo list")
                else:
                    self.log(WARNING_NO_CENTROID,
                             f"Can't find the centroid for cluster {id_cluster}",
                             id_cluster=id_cluster,
                             location=cluster.get("location", ""))

        new_clusters = clusterize(data_images, ESP_KM)
        self.clusters.update(new_clusters)

        return self.clusters

    def _create_clusters_from_path(self, path: str) -> dict:
        data_images = load_images_from_dir(path)

        if not data_images:
            print(f"Can't found : {path}")
            return {}

        return clusterize(data_images, ESP_KM)

    def process(self):
        path_photos_dir = os.environ.get(UNSORTED_PHOTOS_PATH_VAR, DEFAULT_PHOTOS_DIR_PATH)
        if self.clusters is None:
            self.clusters = self._create_clusters_from_path(path_photos_dir)
        else:
            self.clusters = self._update_clusters_with_coord(path_photos_dir)
