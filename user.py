from func.tg_user import client
# from telethon import events
# from telethon.tl.types import UpdateNewMessage, UpdateNewChannelMessage

print(client.get_me())

# client.send_message('kosyachniy', 'Hello World from Telethon!')

chat = client.get_entity('t.me/inst_admins')
print(chat)

# def replier(update):
# 	if isinstance(update, (UpdateNewMessage, UpdateNewChannelMessage)) and str(update.message.to_id.channel_id) in from_id:
# 		print(update)
# 		text = update.message.message

# 		try:
# 			text += '\n' + update.message.media.caption
# 		except:
# 			pass

# 		print(text)

# client.add_update_handler(replier)
# input('!')
# client.disconnect()

# @client.on(events.NewMessage)
# async def my_event_handler(event):
#	 if 'hello' in event.raw_text:
#		 await event.reply('hi!')

# client.start()
# client.run_until_disconnected()