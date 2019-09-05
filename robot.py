#!/usr/bin/env python
# coding:utf8
import sys
import imp
import numpy as np
import pandas as pd

imp.reload(sys)

import itchat
from itchat.content import *

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
   return msg['Text']

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Content'])

# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
# def text_reply(msg):
# 	#print "here we are!"
# 	itchat.send('稍后会给您回复!', msg['FromUserName'])

# # 自动回复图片等类别消息
# # isGroupChat=False表示非群聊消息
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
# def download_files(msg):
# 	itchat.send('稍后会给您回复！', msg['FromUserName'])

# # 自动处理添加好友申请
# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
# 	itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
# 	itchat.send_msg(u'您好', msg['RecommendInfo']['UserName'])
    
# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息


def testContent(msg):
	str1=str(msg['Text'])
	if len(msg['Text'])>50:
		return True
	elif ("实习" in str1):
		return True
	elif("私戳" in str1 ) or ("pm" in str1 ) or ("私聊" in str1 ):
		return True
	else:
		return False

@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	group_name= chatrooms_rename.get(chatroom_id)
	Individual_username = msg['ActualNickName']
	nick_name=chatrooms_nickname.get(chatroom_id)

	print("Chatroom ID: "+chatroom_id)
	print(Individual_username)
	print(msg['Text'])

	# print("length: "+len(msg['Text']))

	id4=chatrooms_group2ID.get("Group4")

	# itchat.send('本消息由自动转发机器人转发[测试中]\n %s—%s 说:\n \n%s' % (nick_name,Individual_username, msg['Content']), userName1)

	if msg['Type'] == TEXT:
		content = msg['Content']
		#print 1
	elif msg['Type'] == SHARING:
		content = msg['Text']

	if (msg['Type'] == TEXT) and (group_name!="Group4") and testContent(msg):
		itchat.send('本消息由自动转发机器人转发[测试中]\n %s—%s 说:\n \n%s' % (nick_name,Individual_username, msg['Content']), userName1)
	elif msg['Type'] == SHARING:
		itchat.send('本消息由自动转发机器人转发[测试中]\n %s—%s 说:\n \n%s' % (nick_name,Individual_username, msg['Text']), userName1)


	print("test get group name: "+str(group_name))

	# if (group_name!="Group4") and testContent(msg):
	# 	for item in chatrooms:
	# 		print(item)
	# 	#print 3
	# 		if not item['UserName'] == chatroom_id:
	# 			#print 4
	# 			itchat.send('本消息由自动转发机器人转发[测试中]\n %s—%s 说:\n \n%s' % (nick_name,username, msg['Content']), item['UserName'])

	# if (chatroom_id=="@d3a27df357f1602aa4a3f6eaaa1aaa9d"):
	# 	cont=msg['Text']
	# 	itchat.send('这是一个测试： %s—%s 说:\n%s' % ('test','test', cont), "@@6f8053c4d4d5eaf7b69e686dd263f127aa361be82cb23ef0aa8decc266d14ae4")


	# print("chatroom_ids:"+chatroom_ids)

	# 消息并不是来自于需要同步的群
	# if not chatroom_id in chatroom_ids:
	# 	return

	#print "chatroom_id" + chatroom_id
	# 发送者的昵称
	#print "username",username
	#获取群名
	#print 11111, chatrooms_rename

################################################################################


	# 根据消息类型转发至其他需要同步消息的群聊
	# if msg['Type'] == TEXT:
	# 	for item in chatrooms:
	# 		print(item)
	# 		#print 3
	# 		if not item['UserName'] == chatroom_id:
	# 			#print 4
	# 			itchat.send('%s—%s 说:\n%s' % (group_name,username, msg['Content']), item['UserName'])
	# # elif msg['Type'] == SHARING:
	# 	#print 5
	# 	for item in chatrooms:
	# 		if not item['UserName'] == chatroom_id:
	# 			itchat.send('%s-%s 分享：\n%s\n%s' % (group_name,username, msg['Text'], msg['Url']), item['UserName'])

# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息   

@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def group_reply_media(msg):
	# 消息来自于哪个群聊
	chatroom_id = msg['FromUserName']
	# 发送者的昵称
	username = msg['ActualNickName']

	# 消息并不是来自于需要同步的群
	# if not chatroom_id in chatroom_ids:
	# 	return

	# 如果为gif图片则不转发
	if msg['FileName'][-4:] == '.gif':
		return

	# 下载图片等文件
	msg['Text'](msg['FileName'])
	# 转发至其他需要同步消息的群聊
	# for item in chatrooms:
	# 	if not item['UserName'] == chatroom_id:
	# 		itchat.send('这是一个自动转发机器人\n @%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), item['UserName'])

# 扫二维码登录
#itchat.auto_login(hotReload=False)
itchat.auto_login(enableCmdQR=2)
# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
chatroom_ids = [c['UserName'] for c in chatrooms]
# chatroom_rename={}
print ('正在监测的群聊：', len(chatrooms), '个')

# print("chatroom_ids: "+ str(chatroom_ids))
#更改群名 ：  交流群+i
i=1
#for k in chatrooms.keys():
chatrooms_rename={}
chatrooms_nickname={}
chatrooms_group2ID={}

for item in chatrooms:
	chatrooms_rename[str(item['UserName'])]='Group'+str(i)  # 群的ID：Group index
	chatrooms_nickname[str(item['UserName'])]=str(item['NickName']) # 群的ID： 群的真实名称
	chatrooms_group2ID['Group'+str(i)]=str(item['UserName']) #Group Index： 群的ID


	print (item['NickName'])
	print (item['UserName'])
	print ('Group'+str(i))

	i+=1

	# print (chatrooms_rename[item['UserName']])
#重新命名之后的群名
print ('chatrooms_rename'+str(chatrooms_rename))

room = itchat.search_friends(name=r'hahaha')  #这里输入你好友的名字或备注。
# print(room)
userName1 = room[0]['UserName'] ## hahaha 好友对应的id （转发对象）
# print(userName1)

#原始群名
# print ' '.join([item['NickName'] for item in chatrooms])
# 开始监测
itchat.run()