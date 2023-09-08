
from collections import Counter
import pandas as pd

from client import client

def main():
        
    
    with client.read("/alice-in-wonderland.txt", encoding="utf-8") as reader:
        wordcount = Counter(reader.read().split()).most_common(10)

        df = pd.DataFrame(wordcount, columns=["word", "count"])
        print(df)

        df.to_parquet("/word-count.parquet")

        # To-Do: Save the wordcount in a Parquet file and read it again!
        client.upload("/word-count.parquet", "/word-count.parquet", overwrite=True)

if __name__ == "__main__":
    main()