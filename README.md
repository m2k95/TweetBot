# Du3aaAPI TweetBot
A script that fetches a prayer from https://api.du3aa.rest and tweet it

> [!WARNING]
> This script does not work anymore, you can try the new working version at https://github.com/m2kio/TweetBot-v2

## Development
> Requires Python >= 3.5

*It is recomended to create a Python virtual environment for development as below.*
* Create a Python virtual environment `python3 -m venv ./venv`
* Activate the Python virtual environment `source ./venv/bin/activate`
* To deactivate the virtual environemnt, simply run `deactivate`

### Install requirements
`pip install -r requirements.txt`

### Usage
`python app.py [post|test]`

## Required Environment Variables
- Twitter Consumer Key
- Twitter Consumer Secret
- Twitter Access Token Key
- Twitter Access Token Secret

> Get them at https://developer.twitter.com

To set environment variables on macOS or Linux, run the export commands below from the terminal
```bash
export CONSUMER_KEY="YOUR-KEY"
export CONSUMER_SECRET="YOUR-SECRET"
export ACCESS_TOKEN_KEY="YOUR-ACCESS-KEY"
export ACCESS_TOKEN_SECRET="YOUR-ACCESS-SECRET"
```
