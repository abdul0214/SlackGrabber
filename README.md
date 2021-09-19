# BoltSlackGrabber
Python based script for downloading conversation data from Slack workspace

### Slack App Configuration

Slack App Scopes required to run the application and get all the data. 

![Capture5](https://user-images.githubusercontent.com/23482179/134352816-c72e8b32-279a-44c0-a34a-31ed26d29df1.PNG)



### Steps
- create a python virtual env

- add a  file with name '.env' to the root of the virtual env

- .env file should contain following values:

        `SLACK_BOT_TOKEN=xoxb-your-bot-token-here`

        `WORKSPACE_FOLDER_NAME='my_new_folder'`

Install packages as follows OR through `pip install -r packages.txt`

- `pip install --upgrade setuptools`
- `pip install ez_setup`
- `pip install virtualenv`
- `pip install python-dotenv`
- `pip install slack_bolt`
- `pip install pandas`

Create and activate virtual environment (on Windows and named 'grabber')

- `virtualenv grabber`
- `cd grabber`
- `grabber\Scripts\activate`
- `python app.py`

