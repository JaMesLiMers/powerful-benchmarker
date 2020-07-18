from pytorch_metric_learning import losses
import copy
from .base_factory import BaseFactory
from ..utils import common_functions as c_f

class LossFactory(BaseFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from .miner_factory import MinerFactory
        self.miner_factory = MinerFactory

    def _create_general(self, loss_type):
        loss, loss_params = self.getter.get("loss", yaml_dict=loss_type, return_uninitialized=True)
        loss_params = copy.deepcopy(loss_params)
        if loss == losses.MultipleLosses:
            loss_funcs = [self.create({k:v}) for k,v in loss_params["losses"].items()]
            return loss(loss_funcs) 
        if loss == losses.CrossBatchMemory:
            if "loss" in loss_params: 
                loss_params["loss"] = self.create(loss_params["loss"])
            if "miner" in loss_params: 
                self.miner_factory = self.miner_factory(api_parser=self.api_parser, getter=self.getter)
                loss_params["miner"] = self.miner_factory.create(loss_params["miner"])
        if c_f.check_init_arguments(loss, "num_classes") and ("num_classes" not in loss_params):
            loss_params["num_classes"] = self.api_parser.split_manager.get_num_labels("train", "train")
            logging.info("Passing %d as num_classes to the loss function"%loss_params["num_classes"])
        if "regularizer" in loss_params:
            loss_params["regularizer"] = self.getter.get("regularizer", yaml_dict=loss_params["regularizer"])

        return loss(**loss_params)