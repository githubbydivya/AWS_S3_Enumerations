# author:   @githubbydivya
# date:     30/10/2022

import asyncio
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from functools import wraps
from typing import Any

from s3enumerations.scanner import Scanner
from s3enumerations.utils import banner
from quart import Quart, render_template, websocket, request, flash, redirect, url_for
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import json
import plotly
import plotly.express as px

_executor = ThreadPoolExecutor(1)

app = Quart(__name__)

messages = [{'s3bucketname': 'Message One'}]


def parse_args(s3_bucket):
    print(banner())

    parser = ArgumentParser(
        description='Bruteforce AWS s3 buckets using different permutations',
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--prefixes', help='prefixes file to use',
                        default='lists/common_bucket_prefixes.txt')

    parser.add_argument('-l', '--limit', help='rate limit the http requests', default=100, type=int)
    parser.add_argument('-u', '--user-agent', default='aiohttp client 0.17', type=str,
                        help='which user agent to use when sending requests')
    parser.add_argument(
        '-target', '--target', help='which target to scan', default=s3_bucket)

    return parser.parse_args()


@app.route('/enumerate/<s3_bucket>', methods=['GET'])
async def main(s3_bucket) -> Any:
    args = parse_args(s3_bucket)
    scanner_obj = Scanner(
        wordlist_path=args.prefixes,
        target=args.target,
        rate_limit=args.limit,
        user_agent=args.user_agent
    )
    scanner_obj.run()
    return 'Executing S3 Bucket Enumerations'


@app.route('/')
async def landing_page() -> Any:
    return await render_template("home.html")


@app.route('/create/', methods=('GET', 'POST'))
async def create() -> Any:
    if request.method == 'POST':
        s3bucketname = (await request.form)["s3bucketname"]

        if not s3bucketname:
            flash('s3bucketname is required!')
        else:
            messages.append({'s3bucketname': s3bucketname})
            return redirect(url_for('main', s3_bucket=s3bucketname))

    return await render_template('create.html')


@app.route('/dashboard')
async def secureu_dashboard():
    return await render_template('secureu_dashboard.html', graphJSON=generate_secureu_dashboard())


@app.route('/callback', methods=['POST', 'GET'])
async def callback_dashboard():
    return generate_secureu_dashboard(request.args.get("data"))


def generate_secureu_dashboard(status_code='ALL'):
    df = pd.read_csv("secureu_output.txt", sep=",", header=None, names=['URL', 'STATUS_CODE'])

    if status_code == 'ALL':
        temp = pd.DataFrame(df['STATUS_CODE'].value_counts())
        temp.index.name = 'val'
        temp.columns = ['count']
        temp = temp.reset_index()
        temp
        fig = px.pie(temp, names='val', values='count', title='S3 Enumerations Statuses')
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
    else:
        temp = pd.DataFrame(df.loc[df['STATUS_CODE'] == status_code].value_counts())
        temp.index.name = 'val'
        temp.columns = ['count']
        temp = temp.reset_index()
        temp
        fig = px.pie(temp, names='val', values='count', title='S3 Enumerations Statuses')
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
