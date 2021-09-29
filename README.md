# twock

Ping/knock a list of tweets and return reachability issues (deleted/protected/withheld...) #twockknock

## Usage

### Knocking Tweets

```txt
twock knock [OPTIONS] TWEETFILE

  Ping (knock) a list of tweets. Expects file path to CSV with `id` column.

Options:
  --outpath TEXT    Path to output file, will be prefixed with today's date.
                    Default: `errors.ndjson`
  --tkpath TEXT     Path to Twitter API v2 bearer token YAML file. Default:
                    `bearer_token.yaml`
  --sample INTEGER  If given, sample INTEGER number of tweets only
  --help            Show this message and exit.
```

### Authentification

You need to have access to the Twitter V2 API and t obtain a valid bearer token. Replace the template value in `bearer_token.yml` with your actual credentials.

## Developer Install

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Clone repository
3. In the cloned repository's root directory run `poetry install`
4. Run `poetry shell` to start development virtualenv
5. Run `twacapic` to enter API keys. Ignore the IndexError.
6. Run `pytest` to run all tests
