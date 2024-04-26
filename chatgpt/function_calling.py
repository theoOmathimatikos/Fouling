import json, os

from naval_gpt import NavalBrain
from naval_gpt_for_ext_data import NavalBrainExtData


def call_naval_llm(feature_id, ext_data_id=None):
    """This function accesses info from the json file (where we assume that the data 
    provided by the user are saved) and calls the `NavalBrain` class, to pass the data
    to the llm to provide a response."""

    # The feature id should have a 1-1 correspondence with the tables' rows. TODO
    with open("chatgpt/features.json") as file:
        feature = json.load(file)["prompts"]
        feature = [i for i in feature if i["id"]==feature_id][0] 
    
    specific, pair = feature['specific'], feature['params_data']['param_data_pair']
    params, data = feature['params_data']['params'], feature['params_data']['data']

    data = str({params[0]: data}) if pair == 'False' else str({k:v for (k, v) in zip(params, data)})
    ext_data = ext_data_id  # TODO. Change in the future

    if not ext_data:
        br = NavalBrain()
        ans = br.invoke(specific, data)
    
    else:
        br = NavalBrainExtData()
        ans = br.invoke_retrieval_chain(specific, data, ext_data)

    print(ans)
    return ans


if __name__ == "__main__":
    call_naval_llm("table_6_2")
        