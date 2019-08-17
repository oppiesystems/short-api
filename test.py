
import unittest

import summarization
from util import percentage_difference
import json
import time

class TestSummarization(unittest.TestCase):
  def test_summarize(self):
    """
    Test that it can reduce content length
    """

    with open('test/test_data.json') as json_data:
      d = json.load(json_data)
      content_list = d['contentList']

      MODEL = summarization.load_models()

      outputs = []

      for content in content_list:
        start = time.time()

        digest_list = summarization.summarize([content], model=MODEL)

        end = time.time()
        
        digest = digest_list[0]

        test_stats = {
          'time': end - start,
          'inputLength': len(content),
          'outputLength': len(digest),
          'reduction': percentage_difference(digest, content)
        }

        outputs.append(test_stats)

      with open('logs/test_stats.json', 'w') as f:
        json.dump({'outputs': outputs}, f, indent=4)

      for test_stats in outputs:
        self.assertGreater(test_stats['inputLength'], test_stats['outputLength'])

if __name__ == '__main__':
  unittest.main()