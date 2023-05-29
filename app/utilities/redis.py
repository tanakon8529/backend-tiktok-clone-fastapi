
from loguru import logger
from fastapi import HTTPException

# # For Cluster
# from rediscluster import RedisCluster
# # Define a function to get the Redis client for the primary instance
# def get_primary_client():
#     redis_client = None
#     try:
#         # Define the Redis client configuration
#         redis_client = RedisCluster(startup_nodes=[{"host": "dedee-cache-001.ubl8we.ng.0001.apse1.cache.amazonaws.com","port": "6379"}], 
#                                     decode_responses=True,
#                                     skip_full_coverage_check=True)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail='RedisCluster not Connected')
        
#     return redis_client

# For Not Cluster
import redis

def get_primary_client():
    redis_client = None
    try:
        redis_client = redis.Redis(host='dedee-cache-001.ubl8we.ng.0001.apse1.cache.amazonaws.com', port=6379, db=0)
        redis_client.ping()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Redis not Connected')
    return redis_client
