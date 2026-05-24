import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")

token = api.AccessToken(API_KEY, API_SECRET) \
    .with_identity("user1") \
    .with_name("Test User") \
    .with_grants(api.VideoGrants(room_join=True, room="promo-room"))

print(token.to_jwt())