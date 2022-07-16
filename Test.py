from multiprocessing import process
from Connect import Connect
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import pandas as pd
from datetime import datetime
import pytz as tz
from telethon.tl.types import ChatForbidden
from telethon.tl.types import Channel
from telethon.tl.types import ChannelForbidden

#global variables
client=Connect.client()
chats = []
names=[]
links=[]
type_chats=[]

#methods
def filterPerType(type_chat, df):
    df_type = df[df['type']==type_chat]
    return df_type

def Df_to_CSV(variables=[]):
    today = datetime.now()
    today_string = today.strftime("%d-%m-%Y-%H-%M-%S")
    dt={'name':variables[0], 'link':variables[1], 'type':variables[2]}
    df=pd.DataFrame(dt)
    df.drop_duplicates() #delete duplicates
    if len(df.index)>0:
        print('All groups an channels')
        print(df)
        df.to_csv('results/all'+today_string+'.csv', index=False,header=True)
    df_channels=filterPerType('Channel', df)
    if len(df_channels.index)>0:
        print('Channels')
        print(df_channels)
        df_channels.to_csv('results/channels'+today_string+'.csv', index=False,header=True)
    df_groups=filterPerType('Group', df)
    if len(df_groups.index)>0:
        print('Groups')
        print(df_groups)
        df_groups.to_csv('results/groups'+today_string+'.csv', index=False,header=True)
    df_mg=filterPerType('Megagroup', df)
    if len(df_mg.index)>0:
        print('Megagroups')
        print(df_mg)
        df_mg.to_csv('results/megagroups'+today_string+'.csv', index=False,header=True)
    df_gg=filterPerType('Gigagroup', df)
    if len(df_gg.index)>0:
        print('Gigagroups')
        print(df_gg)
        df_gg.to_csv('results/gigagroups'+today_string+'.csv', index=False,header=True)
    df_gf=filterPerType('Group forbidden', df)
    if len(df_gf.index)>0:
        print('Groups forbiden')
        print(df_gf)
        df_gf.to_csv('results/gf'+today_string+'.csv', index=False,header=True)
    df_cf=filterPerType('Channel forbidden', df)
    if len(df_cf.index)>0:
        print('Channel forbidden')
        print(df_cf)
        df_cf.to_csv('results/cf'+today_string+'.csv', index=False,header=True)
    
def getDialogs(offset):
    last_date = None
    chunk_size = 150
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=offset,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    return result

def processChats(chats, j):
    for chat in chats:
        try:
            name=chat.title
            id=chat.id 
            if type(chat)==ChatForbidden:
                link='https://t.me/c/'+str(id)
                if link in links:
                    continue
                print(str(j) + '- ' + "Group Forbidden")
                print(name, link)
                names.append(name)
                links.append(link)
                type_chats.append('Group forbidden')
                j+=1
                continue
            elif type(chat)==ChannelForbidden:
                link='https://t.me/c/'+str(id)
                if link in links:
                    continue
                print(str(j) + '- ' + "Channel Forbidden")
                print(name, link)
                names.append(name)
                links.append(link)
                type_chats.append('Channel forbidden')
                j+=1
                continue
            else:
                username=chat.username        
                if username!=None:
                    link='https://t.me/'+username
                    if link in links:
                        continue
                    print(str(j) + '- ' + "Channel")
                    print(name, link)
                    names.append(name)
                    links.append(link)
                else:
                    link='https://t.me/c/'+str(id)
                    if link in links:
                        continue
                    print(str(j) + '- ' +"Group")
                    print(name, link)
                    names.append(name)
                    links.append(link)
                    type_chats.append('Group')
                    j+=1
                    continue
        except Exception as e:
                link='https://t.me/c/'+str(id)
                if link in links:
                    continue
                print(str(j) + '- ' +"Group")
                print("Exception details: ", e)
                print(name, link)
                names.append(name)
                links.append(link)
                type_chats.append('Group')
                j+=1
                continue
        try:
            if chat.broadcast==True:
                type_chats.append('Channel')
                j+=1
                print('Channel')
            elif chat.gigagroup==True:
                type_chats.append('Gigagroup')
                j+=1
                print('Gigagroup')
            elif chat.megagroup== True:
                type_chats.append('Megagroup')
                j+=1
                print('Megagroup')
            else:
                type_chats.append('Group')
        except:
            continue

offset=0
j=0
dialogs=getDialogs(offset, j)
dialogs_count=dialogs.count
while True:
    print('Offset: ',offset,'Links attached: ', len(links))
    dialogs=getDialogs(offset, j)
    chats.extend(dialogs.chats)
    processChats(chats)
    offset+=150
    links_count=len(links)
    if len(dialogs.chats)<150:
        break
    if links_count>=dialogs_count:
        break
Df_to_CSV([names, links, type_chats])


#g_index = input("Enter a Number: ")
#target_group=groups[int(g_index)]