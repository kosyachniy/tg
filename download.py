import json

from func.tg_user import get_entity, history


# Политика
# 'https://t.me/ATC_ATC', 'https://t.me/otsuka_bld', 'https://t.me/wwwproektmedia', 'https://t.me/kompr', 'https://t.me/deputatdumy', 'https://t.me/boilerroomchannel', 'https://t.me/lentadna', 'https://t.me/tv360ru', 'https://t.me/thebell_io'

GROUPS = ()

for name in GROUPS:
	name = get_entity(name).id

	with open('data/history/{}.json'.format(name), 'w') as file:
		print(history(name), file=file)