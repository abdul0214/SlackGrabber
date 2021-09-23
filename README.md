# BoltSlackGrabber
Python based script for downloading conversation and related user data from Slack workspace.

### Slack App Configuration

Slack App Scopes required to run the application and get all the data. 

![image](https://user-images.githubusercontent.com/23482179/134361917-a47f9a06-2408-463b-b789-7acc9768fe40.png)

### Steps
- create a python virtual env

- add a  file with name '.env' to the root of the virtual env

- .env file should contain following values:

        `SLACK_BOT_TOKEN=xoxb-your-bot-token-here`
        `SLACK_SIGNING_SECRET=xoxb-your-bot-secret-here`
        `WORKSPACE_FOLDER_NAME='my_new_folder'`

- copy SlackGrabber.py and app.py to the virtual environment folder (in this case 'grabber')

Install packages as follows OR through `pip install -r packages.txt`

- `pip install --upgrade setuptools`
- `pip install ez_setup`
- `pip install virtualenv`
- `pip install python-dotenv`
- `pip install slack_bolt`
- `pip install pandas`

Create and activate virtual environment (on Windows and named 'grabber')

- `virtualenv grabber`
- `grabber\Scripts\activate`
- `python app.py`

Create and activate virtual environment (on Mac and named 'grabber')

- `virtualenv grabber`
- `source grabber/bin/activate`
- `python app.py`
