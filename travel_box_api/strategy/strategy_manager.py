import pkgutil
import importlib
import inspect

from travel_box_api.utils.manage_json_file import read_json_file
from travel_box_api.utils.manage_json_file import write_json_file
from travel_box_api.utils.singleton import Singleton

from travel_box_api.error.cluster_file_json_error import CantFindClusterJson

import travel_box_api.strategy
from travel_box_api.strategy.strategy import Strategy

from travel_box_api.data.log import INFO_LOADING_DATA, INFO_WRITING_DATA, INFO_END_PROCESS, INFO_RUN_STRATEGIES, log


class StrategyManager(metaclass=Singleton):
    def __init__(self):
        self.SERVICE_CODE = "100"
        self.clusters = None
        self.strategies = self.__load_strategies()

    def __load_strategies(self):
        strategies = {}
        for _, module_name, _ in pkgutil.iter_modules(travel_box_api.strategy.__path__):
            if "_strategy" not in module_name:
                continue
            module = importlib.import_module(f"travel_box_api.strategy.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Strategy) and obj is not Strategy:
                    strategies[obj.__name__] = obj()

        return strategies

    def load_data(self):
        """
        Charge les données nécessaires pour le traitement.
        """
        try:
            self.clusters = read_json_file()
        except CantFindClusterJson:
            self.clusters = None

    def process(self):
        """
        Traite les données chargées.

        Raises:
            NotImplementedError: Cette méthode doit être implémentée par les sous-classes.
        """
        raise NotImplementedError("La méthode 'process' doit être implémentée par les sous-classes.")

    def save_results(self):
        """
        Sauvegarde les résultats du traitement.
        """
        write_json_file(self.clusters)

    def run_sequence(self, sequence, **kwargs):
        log(INFO_RUN_STRATEGIES, f"Run strategies {sequence}", self.SERVICE_CODE)

        log(INFO_LOADING_DATA, "Loading data ...", "000")
        self.load_data()

        return_strategy = None
        strategy_running = None

        for strategy in sequence:
            if isinstance(strategy, dict):
                for strat, args in strategy.items():
                    strategy_running = self.strategies[strat]
                    try:
                        params = {arg: kwargs[arg] for arg in args}
                        return_strategy = strategy_running.run(clusters=self.clusters, **params)
                    except KeyError as e:
                        log("ERROR_0002", f"Can found arg {e}", "000")
                        raise KeyError

            elif isinstance(strategy, str):
                strategy_running = self.strategies[strategy]
                return_strategy = strategy_running.run(self.clusters)
            else:
                log("ERROR_0001", "Paramater not reconized {strategy}", self.SERVICE_CODE)
            self.clusters = strategy_running.clusters

        log(INFO_WRITING_DATA, "Writing data", "000")
        self.save_results()

        log(INFO_END_PROCESS, "End of process", "000")
        return return_strategy
