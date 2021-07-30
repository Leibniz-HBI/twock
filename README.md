# twock
Ping a list of tweets for their status (deleted/available/...) #twocktwock

So far this is only a prototype in `notebooks/`. It will become a CLI tool installable via pip, and maybe integrated in twacapic.

## Developer Install

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Clone repository
3. In the cloned repository's root directory run `poetry install`
4. Run `poetry shell` to start development virtualenv
5. Run `twacapic` to enter API keys. Ignore the IndexError.
6. Run `pytest` to run all tests
