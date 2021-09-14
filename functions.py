def getChannels(channels):
    overall_channels = 0
    overall_messages = 0

    # print("\nfound channels: ")
    # for channel in channels:
    #     print("channel name is ",channel['name'])

    for result in channels:
        for channel in result["channels"]:
            print("channel name is ",channel['name'])
    # if not dryRun:
    #     parentDir = path+"/channels"
    #     mkdir(parentDir)
    #     for channel in channels:
    #         channel_name = channel['name'].encode('utf-8').strip()
    #         channel_name = channel_name.decode('utf-8')
    #         print("getting history for channel {0}".format(channel_name))
    #         fileName = "{parent}/{file}.json".format(parent=parentDir, file=channel_name)
    #         messages = getHistory(s2.conversations, channel['id'])
    #         channelInfo = slack.conversations.info(channel['id']).body['channel']
    #         members_array = []
    #         try:
    #         	members_array =  slack.conversations.members(channel['id']).body['members']
    #         except slacker.Error as e:
    #         	print(e)
    #         	members_array = [repr(e)]
    #         members = {"members":members_array}
    #         channelInfo.update(members)
    #         with open(fileName, 'w') as outFile:
    #             print("writing {0} records to {1}".format(len(messages), fileName))
    #             overall_messages = overall_messages + len(messages)
    #             overall_channels = overall_channels + 1
    #             json.dump({'channel_info': channelInfo, 'messages': messages}, outFile, indent=4)

    # print(("{om} messages in {oc} channels").format(om=overall_messages, oc=overall_channels))

