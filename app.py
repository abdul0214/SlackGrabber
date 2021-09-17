from dotenv import load_dotenv
import os
import logging
import os
import json
from pprint import pprint
import re
import pandas as pd
import ast
# import functions
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
load_dotenv() 
print(os.environ.get("SLACK_BOT_TOKEN"))

# get basic info about the slack channel to ensure the authentication token works
def doTestAuth():
    testAuth = client.auth_test()
    teamName = testAuth['team']
    currentUser = testAuth['user']
    print("Successfully authenticated for team {0} and user {1} ".format(teamName, currentUser))
    print(testAuth)
    return testAuth

def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
channel_name = "general"
conversation_id = None

def getHistory(channelId):
    messages = []
    limit=9999999999999
    cursor = None
    while (True):
        response = client.conversations_history(channel=channelId,cursor=cursor,limit=limit)
        messages.extend(response['messages'])
        if (response['has_more'] == True):
            print('has more')
            cursor = response['response_metadata']['next_cursor']
        else:
            break
    return messages

# fetch all users for the channel and return a map userId -> userName
def getUserMap(path):
    # get all users in the slack organization
    users = client.users_list()['members']
    userIdNameMap = {} 
    userColumns = ['id', 'name', 'real-name', 'email']
    usersDf = pd.DataFrame(columns = userColumns)

    for user in users:
        email = 'none'
        try:
            email = str(user['profile']['email'])
            newRow = pd.Series([user['id'], user['name'], user['profile']['real_name'], email], index=userColumns)
            usersDf = usersDf.append(newRow, ignore_index=True)
        except KeyError as e:
            print ('no email for ' + user['name'])

        if 'email' in user['profile'].keys():
        	print(user['profile']['email'])

        userIdNameMap[user['id']] = user['name']

    usersDf.to_csv(path+'/users.csv', sep=',', index=False, encoding='utf-8')

    print("found {0} users ".format(len(users)))

    return userIdNameMap

def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def getChannels(path, data):
    overall_channels = 0
    overall_messages = 0

    # print("\nfound channels: ")
    # for channel in channels:
    #     print(channel['name'])

    for result in data:
        channels = result["channels"]
        parentDir = path+"/channels"
        mkdir(parentDir)
        for channel in channels:
            channel_name = channel['name'].encode('utf-8').strip()
            channel_name = channel_name.decode('utf-8')
            print("getting history for channel {0} id {1}".format(channel_name,channel['id']))
            fileName = "{parent}/{file}.json".format(parent=parentDir, file=channel_name)
            messages = getHistory(channel['id'])
            members_array = []
            conversation_history = []
            try:
                members_array =  client.conversations_members(channel=channel['id'])['members']
                print('members_array ',members_array)
            except SlackApiError as e:
                members_array=[repr(e)]
                print(e)
                logger.error("Error getting members: {}".format(e))
            members = {"members":members_array}
            channelInfo = channel
            channelInfo.update(members)
            with open(fileName, 'w') as outFile:
                print("writing {0} records to {1}".format(len(messages), fileName))
                overall_messages = overall_messages + len(messages)
                overall_channels = overall_channels + 1
                # print('channel is ', channelInfo)
                # print('channel is ', channelInfo.__repr__)
                # print(channelInfo)
                # p = re.compile('(?<!\\\\)\'')
                # channelInfo = p.sub('\"', str(channel))
                # channelInfo = str(channelInfo).replace("\'", "\"")
                # channelInfo =  json.loads(channelInfo)
                # print("printed ",json.dumps(str(channelInfo)))
                json.dump({'channel_info': channelInfo, 'messages': messages}, outFile, indent=4)
            print("messages found in {} are : \n {}".format(channel['name'],conversation_history ))
            logger.info("{} messages found in {}".format(len(conversation_history), channel['name']))


try:
    path = os.environ.get("WORKSPACE_FOLDER_NAME")
    # Call the conversations.list method using the WebClient
    testAuth = doTestAuth()
    userIdNameMap = getUserMap(path)
    with open(path+'/metadata.json', 'w') as outFile:
        print("writing metadata")
        metadata = {
            "auth_info":ast.literal_eval(str(testAuth).replace("\'", '\"')),
            'users': userIdNameMap
        }
        json.dump(metadata, outFile, indent=4)
    # getChannels(data=client.conversations_list(),path=path)
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


# fetches the complete message history for a channel/group/im
#
# pageableObject could be:
# slack.channel
# slack.groups
# slack.im
#
# channelId is the id of the channel/group/im you want to download history for.
