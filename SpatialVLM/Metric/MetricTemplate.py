import re
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd

class MetricTemplate:

    def __init__(self, **kwargs):

        mapping_dict = kwargs.get("mapping", None)

        if mapping_dict is None:

            mapping_dict = {
                0: "Next Round",
                1: "leftward",
                2: "rightward",
            }

        self.option_map = mapping_dict

        self.result_dict = []
   
    def _extract_info(self, text):

        ans_match = re.search(r"<ans>.*?(\d+).*?</ans>", text)
        ans = int(ans_match.group(1)) if ans_match else None

        rsn_match = re.search(r"<rsn>\s*(.*?)(?:\s*</rsn>|$|\s*<ques>)", text, re.DOTALL)
        rsn = rsn_match.group(1) if rsn_match else "None"

        ques_match = re.search(r"<ques>\s*(.*?)(?:\s*</ques>|$)", text, re.DOTALL)
        ques = ques_match.group(1) if ques_match else "None"

        return ans, rsn, ques
        
    def process_conclusion(self):

        raise NotImplementedError("Subclasses must implement the process_conversations method.")    
    
    def evaluate(self):

        raise NotImplementedError("Subclasses must implement the evaluate method.")

# Subclass for `012` classification task (Left, Right, Uncertain)
class Metric012(MetricTemplate):

    def __call__(self, round_num, conclusion_from_LLM, metadata_dict):

        self.round_num = round_num
        self.conclusion = conclusion_from_LLM
        self.metadata = metadata_dict

        self.process_conclusion()

    def process_conclusion(self):

        self.ans, self.rsn, self.ques = self._extract_info(self.conclusion)

        self.result_one_round = {
            "scene": self.metadata["scene"],
            "seq": self.metadata["seq"],
            "pair": self.metadata["pair"],
            "dof": self.metadata["significance"],
            "label text": self.metadata["significance_text"],
            "label value": self.metadata["significance_value"],
            "round idx": self.round_num,
            "pred option": self.ans,
            "pred text": self.option_map[self.ans],
            "reason": self.rsn,
            "question": self.ques,
        }

        self.result_dict.append(self.result_one_round)
    
    def _evaluate(self):

        stat = Stat012(self.result_dict)

        results = stat._calculate_metrics()

        return results

# Class to calculate evaluation metrics for the `012` classification task
class Stat012:

    def __init__(self, result_dict):

        self.data = pd.DataFrame(result_dict)

    def _calculate_metrics(self):

        max_round = self.data["round idx"].max()

        stat = {}

        summary = self.data.loc[self.data.groupby(['scene', 'seq', 'pair'])['round idx'].idxmax()]

        total_samples = len(summary)
        count_zero = len(summary[summary["pred option"] == 0])
        zero_percentage = count_zero / total_samples * 100

        filtered_data = summary[summary["pred option"] != 0]

        y_true = filtered_data["label text"]
        y_pred = filtered_data["pred text"]

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, pos_label="leftward")
        recall = recall_score(y_true, y_pred, pos_label="leftward")
        f1 = f1_score(y_true, y_pred, pos_label="leftward")

        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred, labels=["leftward", "rightward"])

        # Return the metrics as a dictionary
        scalar_metrics = {
            # "info": ["phi (left, right), 1 round experiment"],
            "length of dataset": [total_samples],
            "not finished percentage": [zero_percentage],
            "accuracy": [accuracy],
            "precision": [precision],
            "recall": [recall],
            "f1_score": [f1],
        }

        metrics = {
            "scalar metrics": scalar_metrics,
            "confusion matrix": cm
        }

        stat[f"summary stat"] = metrics

        for round in range(1, max_round+1):

            round_stat = self.data[self.data["round idx"] == round]

            total_samples = len(round_stat)
            count_zero = len(round_stat[round_stat["pred option"] == 0])
            zero_percentage = count_zero / total_samples * 100

            filtered_data = round_stat[round_stat["pred option"] != 0]

            y_true = filtered_data["label text"]
            y_pred = filtered_data["pred text"]

            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, pos_label="leftward")
            recall = recall_score(y_true, y_pred, pos_label="leftward")
            f1 = f1_score(y_true, y_pred, pos_label="leftward")

            # Confusion Matrix
            cm = confusion_matrix(y_true, y_pred, labels=["leftward", "rightward"])

            # Return the metrics as a dictionary
            scalar_metrics = {
                # "info": ["phi (left, right), 1 round experiment"],
                "length of dataset": [total_samples],
                "not finished percentage": [zero_percentage],
                "accuracy": [accuracy],
                "precision": [precision],
                "recall": [recall],
                "f1_score": [f1],
            }

            metrics = {
                "scalar metrics": scalar_metrics,
                "confusion matrix": cm
            }

            stat[f"{round} round stat"] = metrics

        return stat

if __name__ == "__main__":

    pass
