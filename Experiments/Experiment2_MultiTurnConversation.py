import argparse
import logging

import sys
sys.path.append("./")

from SpatialVLM.logging.logging_config import setup_logging
from SpatialVLM.Conversation.utils import load_process

def parse_args():

    parser = argparse.ArgumentParser(
        description="Run Conversation Experiment pipeline"
        )
    
    parser.add_argument(
        "--data_path", 
        type=str, 
        default="./data/images_conversation", 
        help="path for data stream", 
        required=False
        )
    
    parser.add_argument(
        "--subset", 
        type=str, 
        default="phi", 
        help="path for data stream", 
        required=False
        )

    parser.add_argument(
        "--VLM", 
        type=str, 
        default="llava-hf/llava-v1.6-mistral-7b-hf", 
        required=False
        )
    
    parser.add_argument(
        "--LLM", 
        type=str, 
        default="meta-llama/Meta-Llama-3-8B-Instruct", 
        required=False
        )
    
    parser.add_argument(
        "--mode", 
        type=str, 
        default="single", 
        choices=["single", "pair"], 
        required=False
        )
    
    parser.add_argument(
        "--result_path", 
        type=str, 
        default="./Result/Pair Conversation Experiment/", 
        help="path for result", 
        required=False
        )

    parser.add_argument(
        "--max_len_conv",
        type=int,
        default=10,
        help="length max_len_conv conversation",
        required=False
    )
    
    return parser.parse_args()

def main(args):

    # 0. Logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Mode: {args.mode}")
    logger.info(f"LLM: {args.LLM}")
    logger.info(f"VLM: {args.VLM}")
    logger.info(f"DataPath: {args.data_path}")
    logger.info(f"Subset: {args.subset}")
    logger.info(f"ResultPath: {args.result_path}")

    # 1. Global Config Args
    kwargs = {
        "VLM_id": args.VLM,
        "LLM_id": args.LLM,
        "datapath": args.data_path,
        "subset": args.subset,
        "result dir": args.result_path,
        "len of conversations": args.max_len_conv
    }

    # 2. Load and Run Pipeline
    pipeline = load_process(type="pair", **kwargs)
    pipeline()

if __name__ == "__main__":

    args = parse_args()
    
    main(args)
