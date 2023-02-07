import json
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def __init__(self):
        super().__init__()
        self.output_dtype = []

    def initialize(self, args):
        print("Preprocessing of the Peptide_input")
        model_config = json.loads(args["model_config"])
        output0_config = pb_utils.get_output_config_by_name(model_config, "ce_norm")
        print("preprocess_peptide type: " + str(output0_config))
        self.output_dtype = pb_utils.triton_string_to_numpy(output0_config["data_type"])

    def execute(self, requests):
        responses = []
        for request in requests:
            raw = pb_utils.get_input_tensor_by_name(request, "ce_raw")
            norm = raw.as_numpy() * 0.01
            ce_tensor = pb_utils.Tensor("ce_norm", norm.astype(self.output_dtype))
            responses.append(pb_utils.InferenceResponse(output_tensors=[ce_tensor]))
        return responses

    def finalize(self):
        print("done processing Preprocess")
