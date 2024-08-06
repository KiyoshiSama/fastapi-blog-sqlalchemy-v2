import redis

def create_redis():
  return redis.ConnectionPool(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True
  )

pool = create_redis()