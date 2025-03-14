from SpatialVLM.Conversation import (
    Conversations_Single_Image,
    Conversations_Pairwise_Image
)

def load_process(type, **kwargs):
    
    """
    
    kwargs:
        VLM_id
        LLM_id
        datapath
        subset
    
    """

    process_mapping = {
        "single": Conversations_Single_Image,
        "pair": Conversations_Pairwise_Image
    }

    if type not in process_mapping:
        raise NotImplementedError(f"Type of process {type} not supported.")

    return process_mapping[type](**kwargs)

