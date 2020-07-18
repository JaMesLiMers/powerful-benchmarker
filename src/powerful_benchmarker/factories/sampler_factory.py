import copy
from .base_factory import BaseFactory
from ..utils import common_functions as c_f

class SamplerFactory(BaseFactory):
    def _create_general(self, sampler_type):
        sampler, sampler_params = self.getter.get("sampler", yaml_dict=sampler_type, return_uninitialized=True)
        sampler_params = copy.deepcopy(sampler_params)
        if c_f.check_init_arguments(sampler, "labels"):
            sampler_params["labels"] = self.api_parser.split_manager.get_labels("train", "train")
        if sampler_params.get("length_before_new_iter") == "dataset_length":
            sampler_params["length_before_new_iter"] = len(self.api_parser.split_manager.get_dataset("train", "train"))
            logging.info("Set sampler length_before_new_iter to {}".format(sampler_params["length_before_new_iter"]))
        return sampler(**sampler_params)
               