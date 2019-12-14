# Одно ключевое слово

curl -X POST -H "Content-Type: application/json" -d '{"method": "discussions.analytics", "params": {"tags": "Керчь"}, "token": "owner"}' http://127.0.0.1:5000/

# Несколько ключевых слов

curl -X POST -H "Content-Type: application/json" -d '{"method": "discussions.analytics", "params": {"tags": ["биткоин", "криптовалюта", "крипта", "crypto", "cryptocurrency", "btc", "eth", "ltc", "майнинг", "mining"]}, "token": "owner"}' http://127.0.0.1:5000/

# Тренды

curl -X POST -H "Content-Type: application/json" -d '{"method": "trends.get", "params": {"search": "Керчь"}, "token": "owner"}' http://127.0.0.1:5000/