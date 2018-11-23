from func.tg_user import client
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
# from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel

channel = client.get_entity(1091219672) # 1142824902)
print(channel)

# offset = 0
# limit = 200
# my_filter = ChannelParticipantsSearch('')
# all_participants = []

# # # result = client(GetParticipantsRequest(InputChannel(1091219672, -6011616057149755187)))
# # # print(result)

# # # channel = client(GetFullChannelRequest('boilerroomchannel'))

# participants = client(GetParticipantsRequest(channel=channel, filter=my_filter, offset=offset, limit=limit, hash=0))
# print(participants)

print(client(GetFullChannelRequest(channel)))