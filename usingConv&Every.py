#Pulls info from conversation.json and everyone.json, the issue is that conversation.json only has the most recent 66 posts and everyone.json does not contain ALL users for some reason. In all, the data was cleaner than message.json, but insufficient. 
import json
import matplotlib.pyplot as plt
# Load JSON data about the group members
with open('C:\\Users\\jdog1\\OneDrive\\Documents\\Spring2024\\Data Science Projects\\Delta Quotes Analysis\\Exported GM chat Data\\conversation.json', 'r', encoding='utf-8') as file:
    group_data = json.load(file)

# Create a mapping from user IDs to names
user_id_to_name = {member['user_id']: member['name'] for member in group_data['members']}
with open('C:\\Users\\jdog1\\OneDrive\\Documents\\Spring2024\\Data Science Projects\\Delta Quotes Analysis\\Exported GM chat Data\\everyone.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize dictionaries to store the count of likes for each user and the number of times each user has liked posts
likes_count = {}
total_likes_per_user = {}

# Iterate over each message object
for message in data['response']['messages']:
    # Extract the list of user IDs who liked this message
    favorited_by = message.get('favorited_by', [])
    
    # Increment the count of likes for each user and calculate the total number of likes per user
    for user_id in favorited_by:
        likes_count[user_id] = likes_count.get(user_id, 0) + 1
        total_likes_per_user[user_id] = total_likes_per_user.get(user_id, 0) + len(favorited_by)

# Replace user IDs with names in the dictionaries
likes_count = {user_id_to_name.get(user_id, user_id): count for user_id, count in likes_count.items()}
total_likes_per_user = {user_id_to_name.get(user_id, user_id): count for user_id, count in total_likes_per_user.items()}

# Calculate the average number of likes received by each user
average_likes_per_user = {user_id_to_name.get(user_id, user_id): total_likes_per_user[user_id] / likes_count[user_id] for user_id in likes_count}

# Sort dictionaries by values (number of likes)
sorted_average_likes_per_user = dict(sorted(average_likes_per_user.items(), key=lambda item: item[1]))
sorted_likes_count = dict(sorted(likes_count.items(), key=lambda item: item[1]))

# Plot the average number of likes received by each user
plt.figure(figsize=(12, 8))
plt.bar(sorted_average_likes_per_user.keys(), sorted_average_likes_per_user.values())
plt.xlabel('Users')
plt.ylabel('Average Likes per Post')
plt.title('Average Number of Likes Received by Each User')
plt.xticks(rotation=85, ha='right')
plt.tight_layout()
plt.show()

# Plot the number of times each user has liked posts
plt.figure(figsize=(12, 8))
plt.bar(sorted_likes_count.keys(), sorted_likes_count.values())
plt.xlabel('User')
plt.ylabel('Number of Likes')
plt.title('Number of Times Each User Has Liked Posts')
plt.xticks(rotation=85, ha='right')
plt.tight_layout()
plt.show()