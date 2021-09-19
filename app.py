from dotenv import load_dotenv
import os
from SlackGrabber import SlackGrabber

load_dotenv() 
path = os.environ.get("WORKSPACE_FOLDER_NAME")
botToken = os.environ.get("SLACK_BOT_TOKEN")

slackGrabber = SlackGrabber(path = path, botToken = botToken) 
slackGrabber.doTestAuth()
slackGrabber.getChannels()
slackGrabber.getMetadata()
