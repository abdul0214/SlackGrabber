from dotenv import load_dotenv
import os
import logging
import os
import functions
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
load_dotenv() 
print(os.environ.get("SLACK_BOT_TOKEN"))
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
channel_name = "general"
conversation_id = None
try:
    # Call the conversations.list method using the WebClient
    functions.getChannels(client.conversations_list())
    # for result in client.conversations_list():
    #     if conversation_id is not None:
    #         break
    #     for channel in result["channels"]:
    #         print(channel["name"],channel[''])
            # if channel["name"] == channel_name:
            #     conversation_id = channel["id"]
            #     #Print result
            #     print(f"Found conversation ID: {conversation_id}")
            #     break

except SlackApiError as e:
    print(f"Error: {e}")