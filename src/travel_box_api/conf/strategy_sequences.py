# Request's data are passed by the data arg

SEQUENCES = {
    "GET": {
        "/group_photo_by_location": {
            "STRATEGIES": [
                "GroupPhotosByLocationStrategy",
                "BuildLocationPropStrategy",
                "ImportFromDirStrategy",
                "SplitUrbanClustersStrategy",
                "ComputeCentroidStrategy",
                "FindPlaceNameStrategy",
                "ClusterGeocodingStrategy",
                "ClusterTimeRangeStrategy",
                "ComputeFarestDistanceStrategy",
                "BuildLocationPropStrategy",
                "MergeClusterSameLocationStrategy"
            ]
        },
        "/batch/find_urban_clusters": {
            "STRATEGIES": [
                "SplitUrbanClustersStrategy",
                "ComputeCentroidStrategy"
            ]
        },
        "/batch/group_photo_by_location": {
            "STRATEGIES": [
                "ComputeCentroidStrategy",
                "GroupPhotosByLocationStrategy",
            ]
        },
        "/batch/import_from_dir": {
            "STRATEGIES": [
                "ImportFromDirStrategy",
            ]
        },
        "/batch/find_place_name": {
            "STRATEGIES": [
                "FindPlaceStrategy"
            ]
        },
        "/batch/cluster_geocondig": {
            "STRATEGIES": [
                "ClusterGeocodingStrategy"
            ]
        },
        "/batch/export_as_gpx": {
            "STRATEGIES": [
                "ExportClusterGPXStrategy"
            ]
        },
        "/cluster/<uuid:cluster_id>": {
            "STRATEGIES": [
                {"GetClusterStrategy": ["cluster_id"]}
            ]
        },
        "/clusters/": {
            "STRATEGIES": [
                "GetClustersStrategy"
            ]
        },
        "/map_cluster": {
            "STRATEGIES": [
                "GetClusterMapStrategy"
            ]
        },
        "/stat_clusters": {
            "STRATEGIES": [
                "GetClustersStatStrategy"
            ]
        },
    },
    "POST": {
        "/photo/add_tags/<string:photo_id>": {
            "STRATEGIES": [
                {"AddPhotoTagsStrategy": ["photo_id", "data"]},
            ]
        }
    },
    "UPDATE": {
        "/cluster/<string:cluster_id>": {
            "STRATEGIES": [
                {"UpdateClusterStrategy": ["cluster_id", "data"]},
                "BuildLocationPropStrategy",
                "MergeClusterSameLocationStrategy",
                "ComputeCentroidStrategy",
                "ComputeFarestDistanceStrategy",
            ]
        }
    },
    "DELETE": {
        "/cluster/<string:cluster_id>/<string:photo_id>": {
            "STRATEGIES": [
                {"DeletePhotoFromClusterStrategy": ["cluster_id", "photo_id"]},
                "ComputeCentroidStrategy",
                "ComputeFarestDistanceStrategy",
            ]
        }
    }
}
