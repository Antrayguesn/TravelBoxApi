import json
import os

from travel_box_api.error.cluster_file_json_error import CantFindClusterJsonError, CantReadClusterJsonError

PATH_TO_DATA_FILE_VAR = "TB_PATH_TO_DATA_FILE_DIR"
DEFAULT_DATA_FILE = "."


def read_json_file() -> dict:
    path_to_data_file = os.environ.get(PATH_TO_DATA_FILE_VAR, DEFAULT_DATA_FILE)
    try:
        with open(f"{path_to_data_file}/data.json", encoding="utf-8") as clusters_json_file:
            clusters = json.load(clusters_json_file)
    except FileNotFoundError as e:
        raise CantFindClusterJsonError() from e
    except Exception as e:
        raise CantReadClusterJsonError() from e
    return clusters


def write_json_file(clusters: dict):
    path_to_data_file = os.environ.get(PATH_TO_DATA_FILE_VAR, DEFAULT_DATA_FILE)
    with open(f"{path_to_data_file}/data.json", "w", encoding="utf-8") as clusters_json_file:
        json.dump(clusters, clusters_json_file)
