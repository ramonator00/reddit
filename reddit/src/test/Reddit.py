import pandas as pd
import unittest

from reddit.src.framework.SentimentAnalyzer import SentimentAnalyzer


class Reddit(unittest.TestCase):
    def test_sentiment_analysis(self):
        bert = SentimentAnalyzer()

        d = {'title': ['Swiss Banks Are Once Again Investing More']}
        df = pd.DataFrame(data=d)

        df_sentiment = bert.analyze_data(df)

        self.assertGreater(float(df_sentiment['positive']), float(df_sentiment['negative']))


if __name__ == '__main__':
    unittest.main()
