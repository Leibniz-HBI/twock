from datetime import datetime
from math import ceil

import click
import ndjson
import pandas as pd
import yaml

from loguru import logger
from twarc import Twarc2


@click.group()
def cli():
    pass


@cli.command(help='Ping (knock) a list of tweets. Expects file path to CSV with `id` column.')
@click.argument('tweetfile')
@click.option('--outpath', default='errors',
              help="Path to output file, will be prefixed with today's date. Default: `errors.ndjson`")
@click.option('--tkpath', default='bearer_token.yaml',
              help='Path to Twitter API v2 bearer token YAML file. Default: `bearer_token.yaml`')
@click.option('--sample', default=0, help='If given, sample INTEGER number of tweets only')
def knock(tweetfile, outpath, tkpath, sample):

    with open(tkpath) as f:
        bearer_token = yaml.safe_load(f)['bearer_token']

    t = Twarc2(bearer_token=bearer_token, connection_errors=10)

    logger.info('reading tweet file')

    tweets = pd.read_csv(
        tweetfile, lineterminator='\n', dtype=str)

    logger.info('read tweet file')

    ids = tweets['id']

    if sample > 0:
        ids = ids.sample(sample)

    lookup = t.tweet_lookup(ids.values)

    errors = list()

    pages = 0

    logger.info('start knocking')

    for page in lookup:
        pages += 1

        for tweet in page['data']:
            if 'withheld' in tweet.keys():  # check whether tweet is withheld in any country
                errors.append(tweet)  # if so, append tweet object to errors

        page_length = len(page['data'])

        if page_length != 100:  # Now focus on 'incomplete' pages

            if len(ids) >= pages * 100:  # There should be errors if page is not last page
                assert 'errors' in page.keys()

            n = 0

            if 'errors' in page.keys():
                for error in page['errors']:
                    if error['parameter'] == 'ids' and error['resource_type'] == 'tweet':
                        # These fields seem to mark a 'deleted' or 'protected' tweet error

                        # just to be sure that our logic is sound
                        assert error['value'] in ids.values

                        errors.append(error)

                        n += 1

            if len(ids) >= pages * 100:     # If page is not last page
                # the number of errors should explain the missing tweets.
                assert page_length == 100 - n

        logger.info(f'finished page {pages} of {ceil(len(ids) / 100)}')

    assert pages == ceil(len(ids) / 100)    # Have we processed all pages?

    result_path = f'{datetime.strftime(datetime.now(), "%Y%m%d_%H%M")}_{outpath}.ndjson'
    # write to file with today's date in front
    with open(f'{result_path}', 'w') as f:
        ndjson.dump(errors, f)

    logger.info(f'written result to {result_path}')


if __name__ == '__main__':
    cli()
