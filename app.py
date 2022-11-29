from flask import Flask, redirect, url_for, request
import pandas as pd
import numpy as np
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

app = Flask(__name__)

# search through the reviews for a specific product
def search_reviews(df, product_description, n=3, pprint=True):
    embedding = get_embedding(
        product_description,
        engine="text-search-babbage-query-001"
    )
    df["similarities"] = df.babbage_search.apply(lambda x: cosine_similarity(x, embedding))

    res = df.sort_values("similarities", ascending=False).head(n)['text']
    if pprint:
        for r in res:
            print(r[:200])
            print()
    return res

@app.route('/')
def index():
    if request.method == 'POST':
        return 'Calling the Chairman AI Python GET route'
    else:
        df = pd.read_csv('wiki_set.csv')
        df["babbage_search"] = df.babbage_search.apply(eval).apply(np.array)

        openai.api_key = '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'

        res = search_reviews(df, "artificial intelligence", n=3)

        summary_components = []
        for r in res:
            summary_components.append(r)

        new_line = '\n'
        text_prompt = f'Summarize these three articles then combine them into a single article and summarize that article so that the result is a single article that is 500 characters or less in length: 1) {summary_components[0]}{new_line}{new_line} 2) {summary_components[1]}{new_line}{new_line} 3) {summary_components[2]}'

        text_completion = openai.Completion.create(
            model="text-davinci-002",
            prompt=text_prompt,
            max_tokens=510,
            temperature=0
        )
        promptResponse = text_completion['choices'][0].text

        print(promptResponse)

        return promptResponse