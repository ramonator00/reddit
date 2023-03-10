import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class SentimentAnalyzer(object):
    """
    This class generates a sentiment analysis using FinBERT Based on given TextData
    """

    def __init__(self):
        self.__model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.__tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

    def analyze_data(self, data) -> pd.DataFrame:
        """
        This method analyzes data and calculates a sentiment
        :id: id of post
        :data: desired Data as dataframe
        return: exit code 0 if workflow is done -1 if not
        """
        df_arr = np.array(data)
        df_list = list(df_arr[:, 0])

        inputs = self.__tokenizer(df_list, padding=True, truncation=True, return_tensors='pt')
        outputs = self.__model(**inputs)

        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

        positive = predictions[:, 0].tolist()
        negative = predictions[:, 1].tolist()
        neutral = predictions[:, 2].tolist()

        table = {"title": df_list,
                 "positive": positive,
                 "negative": negative,
                 "neutral": neutral}

        df = pd.DataFrame(table, columns=["title", "positive", "negative", "neutral"])

        return df
