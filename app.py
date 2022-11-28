from flask import Flask, redirect, url_for, request
import pandas as pd
import numpy as np
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

app = Flask(__name__)

@app.route('/')
def index():
    if request.method == 'POST':
        return 'Calling the Chairman AI Python GET route'
    else:
        return 'Calling the Chairman AI Python POST route'