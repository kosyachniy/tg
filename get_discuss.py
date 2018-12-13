from func.tg_user import client

import datetime

from telethon.tl import types
from telethon.tl.functions.messages import SearchRequest, SearchGlobalRequest


def get_discuss(text='Керчь'):
	# all = client(SearchRequest(
	# 	peer=types.InputPeerEmpty(),
	# 	q=text,
	# 	filter=types.InputMessagesFilterEmpty(),
	# 	min_date=datetime.datetime(2018, 1, 1),
	# 	max_date=None, # datetime.datetime(2018, 11, 23),
	# 	offset_id=0,
	# 	add_offset=0,
	# 	limit=100,
	# 	max_id=0,
	# 	min_id=0,
	# 	hash=0,
	# 	from_id=None, # types.InputUserEmpty(),
	# ))

	all = client(SearchGlobalRequest(
		q=text,
		offset_date=datetime.datetime.now(), # datetime(2018, 12, 1),
		offset_peer=types.InputPeerEmpty(), # types.InputPeerSelf(),
		offset_id=0,
		limit=3,
	))

	return [i.message for i in all.messages]


if __name__ == '__main__':
	print(*get_discuss(), sep='\n------\n')