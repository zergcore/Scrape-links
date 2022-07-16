from types import NoneType
from Connect import Connect
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import PeerChannel
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import PeerChat
from telethon.tl.types import InputPeerChat
from telethon.tl.types import PeerUser
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types.messages import Messages
import pandas as pd
import asyncio
import json
import datetime
import pytz as tz

client=Connect.client()
#print(client.get_me())

def filterPerType(type_chat, df):
    df_type = df[df['type']==type_chat]
    return df_type

def Df_to_CSV(variables=[]):
    dt={'name':variables[0], 'link':variables[1], 'type':variables[2]}
    df=pd.DataFrame(dt)
    df.drop_duplicates() #delete duplicates
    print('All groups an channels')
    print(df)
    df_channels=filterPerType('Channel', df)
    print('Channels')
    print(df_channels)
    df_groups=filterPerType('Group', df)
    print('Groups')
    print(df_groups)
    df_channels.to_csv('channels.csv', index=False,header=True)
    df_groups.to_csv('groups.csv', index=False,header=True)
    df.to_csv('all.csv', index=False,header=True)

async def main(client):
    await client.start()

    offset_id = 0
    limit = 600
    names=[]
    links=[]
    type_chats=[]
    total_links = 0
    total_count_limit = 0
    # create dictionary of ids to users and chats
    users = {}
    chats = {}
    counter=0
    channel_counter=0
    group_counter=0
    else_counter=0

    while True:
        print("Current Offset ID is:", offset_id, "; Total links:", total_links)
        try:
            dialogs = await client(GetDialogsRequest(
            offset_date=None,
            offset_id=offset_id,
            offset_peer=InputPeerEmpty(),
            limit=limit,
            hash=0
            ))   
        except Exception as e:
            print ("Exception details: ",e)
            await asyncio.sleep(10)
            continue
        if not dialogs.dialogs:
            break
        for u in dialogs.users:
            users[u.id] = u
        for c in dialogs.chats:
            chats[c.id] = c
        for d in dialogs.dialogs:
            counter+=1
            print(counter)
            #print(d.stringify())
            peer = d.peer
            if isinstance(peer, PeerChannel):
                id = peer.channel_id
                channel = chats[id]
                access_hash = channel.access_hash
                name = channel.title
                #offset_id=id
                try:
                    username=channel.username
                    if username!=None:
                        print("Channel")
                        print(name, 'https://t.me/'+username)
                        names.append(name)
                        links.append('https://t.me/'+username)
                        type_chats.append('Channel')
                        channel_counter+=1
                    else:
                        print("Group")
                        print(name, 'https://t.me/c/'+str(id))
                        names.append(name)
                        links.append('https://t.me/c/'+str(id))
                        type_chats.append('Group')
                        group_counter+=1
                except Exception as e:
                    print("Exception details: ", e)
                    print(name, 'https://t.me/c/'+str(id))
                
                input_peer = InputPeerChannel(id, access_hash)
            elif isinstance(peer, PeerChat):
                id = peer.chat_id
                group = chats[id]
                name = group.title
                #offset_id=id
                try:
                    username=group.username
                    if username!=None:
                        print("Group")
                        print(name, 'https://t.me/'+username)
                        names.append(name)
                        links.append('https://t.me/'+username)
                        type_chats.append('Group')
                        group_counter+=1
                    else:
                        print("Group")
                        print(name, 'https://t.me/c/'+str(id))
                        names.append(name)
                        links.append('https://t.me/c/'+str(id))
                        type_chats.append('Group')
                        group_counter+=1
                except Exception as e:
                    print("Exception details: ", e)
                    print(name, 'https://t.me/c/'+str(id))
                input_peer = InputPeerChat(id)
            elif isinstance(peer, PeerUser):
                id = peer.user_id
                user = users[id]
                access_hash = user.access_hash
                name = user.first_name
                offset_id=id
                print("User")
                try:
                    username=user.username
                    if username!=None:
                        print(name, 'https://t.me/'+username)
                    else:
                        print(name, 'https://t.me/c/'+str(id))
                except Exception as e:
                    print("Exception details: ", e)
                    print(name, 'https://t.me/c/'+str(id))
                user_counter+=1
                input_peer = InputPeerUser(id, access_hash)
            else:
                else_counter+=1
                continue
        offset_id +=100
        total_links = len(links)
        total_count_limit=dialogs.count
        lenght_dialogs=len(dialogs.dialogs)
        if lenght_dialogs<100:
            break
        if total_count_limit != 0 and total_links >= total_count_limit:
            break

    Df_to_CSV([names, links, type_chats])



with client:
    client.loop.run_until_complete(main(client))

'''
get_dialogs = GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=10000,
    hash=0
)
dialogs = client(get_dialogs)
#print(dialogs)
dialogs_lenght=dialogs.count
print('dialogs lenght', str(dialogs_lenght))
channel_counter=0
group_counter=0
user_counter=0
else_counter=0
counter=0

# create dictionary of ids to users and chats
counts = {}
users = {}
chats = {}

for u in dialogs.users:
    users[u.id] = u

for c in dialogs.chats:
    chats[c.id] = c


names=[]
links=[]
type_chats=[]
for d in dialogs.dialogs:
    counter+=1
    print(counter)
    peer = d.peer
    if isinstance(peer, PeerChannel):
        id = peer.channel_id
        channel = chats[id]
        access_hash = channel.access_hash
        name = channel.title
        try:
            username=channel.username
            if username!=None:
                print("Channel")
                print(name, 'https://t.me/'+username)
                names.append(name)
                links.append('https://t.me/'+username)
                type_chats.append('Channel')
                channel_counter+=1
            else:
                print("Group")
                print(name, 'https://t.me/c/'+str(id))
                names.append(name)
                links.append('https://t.me/c/'+str(id))
                type_chats.append('Group')
                group_counter+=1
        except Exception as e:
            print("Exception details: ", e)
            print(name, 'https://t.me/c/'+str(id))
        
        input_peer = InputPeerChannel(id, access_hash)
    elif isinstance(peer, PeerChat):
        id = peer.chat_id
        group = chats[id]
        name = group.title
        try:
            username=group.username
            if username!=None:
                print("Group")
                print(name, 'https://t.me/'+username)
                names.append(name)
                links.append('https://t.me/'+username)
                type_chats.append('Group')
                group_counter+=1
            else:
                print("Group")
                print(name, 'https://t.me/c/'+str(id))
                names.append(name)
                links.append('https://t.me/c/'+str(id))
                type_chats.append('Group')
                group_counter+=1
        except Exception as e:
            print("Exception details: ", e)
            print(name, 'https://t.me/c/'+str(id))
        input_peer = InputPeerChat(id)
    elif isinstance(peer, PeerUser):
        id = peer.user_id
        user = users[id]
        access_hash = user.access_hash
        name = user.first_name
        print("User")
        try:
            username=user.username
            if username!=None:
                print(name, 'https://t.me/'+username)
            else:
                print(name, 'https://t.me/c/'+str(id))
        except Exception as e:
            print("Exception details: ", e)
            print(name, 'https://t.me/c/'+str(id))
        user_counter+=1
        input_peer = InputPeerUser(id, access_hash)
    else:
        else_counter+=1
        continue

    get_history = GetHistoryRequest(
        peer=input_peer,
        offset_id=0,
        offset_date=None,
        add_offset=0,
        limit=1,
        max_id=0,
        min_id=0,
        hash=0
    )

    history = client(get_history)
    if isinstance(history, Messages):
        count = len(history.messages)
    else:
        count = history.count

    counts[name] = count

dt={'name':names, 'link':links, 'type':type_chats}
df=pd.DataFrame(dt)
print(df)
df_channels=filterPerType('Channel', df)
print(df_channels)
df_groups=filterPerType('Group', df)
print(df_groups)
'''

'''
df_channels.to_csv('channels.csv', index=False,header=True)
df_groups.to_csv('groups.csv', index=False,header=True)
'''

#print(counts)

'''
print('Channels ', str(channel_counter))
print('Groups ', str(group_counter))
print('user ', str(user_counter))
print('else ', str(else_counter))
'''

'''
c=0
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
for name, count in sorted_counts:
    c+=1
    print(c)
    print('{}: {}'.format(name, count))
'''