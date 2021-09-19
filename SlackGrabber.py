from dotenv import load_dotenv
import os
import logging
import os
import json
from pprint import pprint
import re
import pandas as pd
import ast
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackGrabber:
    def __init__(self, botToken, path):
        self.client = WebClient(token=botToken)
        self.logger = logging.getLogger(__name__)
        self.path = path

    def doTestAuth(self):
        testAuth = self.client.auth_test()
        teamName = testAuth['team']
        currentUser = testAuth['user']
        print("Successfully authenticated for team {0} and user {1} ".format(teamName, currentUser))
        return testAuth
    def mkdir(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
    def getHistory(self, channelId):
        messages = []
        limit=9999999999999
        cursor = None
        while (True):
            response = self.client.conversations_history(channel=channelId,cursor=cursor,limit=limit)
            messages.extend(response['messages'])
            if (response['has_more'] == True):
                print('has more')
                cursor = response['response_metadata']['next_cursor']
            else:
                break
        return messages

    def getUserMap(self):
        users = self.client.users_list()['members']
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
        usersDf.to_csv(self.path+'/users.csv', sep=',', index=False, encoding='utf-8')
        print("found {0} users ".format(len(users)))
        return userIdNameMap
    
    def getChannels(self):
        data = self.client.conversations_list()
        overall_channels = 0
        overall_messages = 0
        for result in data:
            channels = result["channels"]
            parentDir = self.path+"/channels"
            self.mkdir(parentDir)
            for channel in channels:
                channel_name = channel['name'].encode('utf-8').strip()
                channel_name = channel_name.decode('utf-8')
                print("getting history for channel {0} id {1}".format(channel_name,channel['id']))
                fileName = "{parent}/{file}.json".format(parent=parentDir, file=channel_name)
                messages = self.getHistory(channel['id'])
                members_array = []
                conversation_history = []
                try:
                    members_array =  self.client.conversations_members(channel=channel['id'])['members']
                    print('members_array ',members_array)
                except SlackApiError as e:
                    members_array=[repr(e)]
                    print(e)
                    self.logger.error("Error getting members: {}".format(e))
                members = {"members":members_array}
                channelInfo = channel
                channelInfo.update(members)
                with open(fileName, 'w') as outFile:
                    print("writing {0} records to {1}".format(len(messages), fileName))
                    overall_messages = overall_messages + len(messages)
                    overall_channels = overall_channels + 1
                    json.dump({'channel_info': channelInfo, 'messages': messages}, outFile, indent=4)
                print("messages found in {} are : \n {}".format(channel['name'],conversation_history ))
                self.logger.info("{} messages found in {}".format(len(conversation_history), channel['name']))
    def getPrivateChannels(self):
        groups = self.client.users.conversations
        print("\nfound private channels:")
        for group in groups:
            print("{0}: ({1} members)".format(group['name'], len(group['members'])))

        if not dryRun:
            parentDir = self.path+"/channels"
            self.mkdir(parentDir)

            for group in groups:
                messages = []
                print("getting history for private channel {0} with id {1}".format(group['name'], group['id']))
                fileName = "{parent}/{file}.json".format(parent=parentDir, file=group['name'])
                messages = getHistory(slack.groups, group['id'])
                channelInfo = slack.groups.info(group['id']).body['group']
                with open(fileName, 'w') as outFile:
                    print("writing {0} records to {1}".format(len(messages), fileName))
                    json.dump({'channel_info': channelInfo, 'messages': messages}, outFile, indent=4)
    def getMetadata(self):
        try:
            testAuth = self.doTestAuth()
            userIdNameMap = self.getUserMap()
            with open(self.path+'/metadata.json', 'w') as outFile:
                print("writing metadata")
                metadata = {
                    "auth_info":ast.literal_eval(str(testAuth).replace("\'", '\"')),
                    'users': userIdNameMap
                }
                json.dump(metadata, outFile, indent=4)
        except SlackApiError as e:
            print(f"Error: {e}")