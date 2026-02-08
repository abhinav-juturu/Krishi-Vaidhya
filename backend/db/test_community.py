# kvb/db/test_community.py
from .community_service import (
    create_post,
    add_comment,
    like_post,
    get_posts
)

# Create post with location
post_id = create_post(
    user_id="9999999999",
    content="Apple Black Rot seen in my orchard",
    lat=12.9716,
    lng=77.5946
)

print(f"✅ Post created: {post_id}")

# Add comment
add_comment(
    post_id=post_id,
    user_id="8888888888",
    content="Remove infected leaves immediately"
)

# Like post
like_post(
    post_id=post_id,
    user_id="7777777777"
)

# Get posts
posts = get_posts()
print(f"✅ Retrieved {len(posts)} posts")
print(posts[0] if posts else "No posts")