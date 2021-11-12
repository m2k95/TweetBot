# Du3aaAPI TweetBot
A script that fetches a prayer from https://api.du3aa.rest and tweet it at [@du3aaAPI](https://twitter.com/du3aaAPI)

## Development
> Requires Python >= 3.5

*It is recomended to create a Python virtual environment as below.*
* Create a Python virtual environment `python3 -m venv ./venv`
* Activate the Python virtual environment `source ./venv/bin/activate`
* To deactivate the virtual environemnt, simply run `deactivate`

### Install requirements
`pip install -r requirements.txt`

### Usage
`python app.py [post|test]`

### Required ENVs
- Twitter Consumer Key
- Twitter Consumer Secret
- Twitter Access Token Key
- Twitter Access Token Secret

> Get them at https://developer.twitter.com
