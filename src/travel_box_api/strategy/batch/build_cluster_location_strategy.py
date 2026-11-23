from travel_box_api.strategy.strategy import Strategy


class BuildClusterLocationStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.STRATEGY_CODE = "011"

    def __build_location_props(self):
        for cluster in self.clusters.values():
            if cluster.get("location"):
                continue

            parts = [
                cluster.get("continent"),
                cluster.get("country"),
                cluster.get("region"),
                cluster.get("place"),
            ]

            cluster["location"] = "/".join(filter(None, parts))

    def process(self):
        self.__build_location_props()
