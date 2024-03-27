import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load JSON data about the group members
with open('C:\\Users\\jdog1\\OneDrive\\Documents\\Spring2024\\Data Science Projects\\Delta Quotes Analysis\\Exported GM chat Data\\conversation.json', 'r', encoding='utf-8') as file:
    group_data = json.load(file)

# Create a mapping from user IDs to names
user_id_to_name = {member['user_id']: member['name'] for member in group_data['members']}

# Manually add missing user IDs and names to the user_id_to_name dictionary
user_id_to_name.update({
    '94842236': 'Suhas G',
    '58304457': 'Charlie Breen',
    '85801105': 'Jack Kirkhorn',
    '61294173': 'Will Gawrylowicz',
    '22421689': 'Austin Hanley',
    '39577603': 'Adity Kannoth',
    '27270670': 'Alex Prince',
    '32621779': 'Bart Turney',
    '61977517': 'Luca Finkbeiner'
})

# Load JSON data from message.json
with open('C:\\Users\\jdog1\\OneDrive\\Documents\\Spring2024\\Data Science Projects\\Delta Quotes Analysis\\Exported GM chat Data\\message.json', 'r', encoding='utf-8') as file:
    message_data = json.load(file)

# Initialize dictionaries to store the count of likes for each user, the number of posts by each user,
# and the total number of likes given by each user
likes_count = {}
posts_count = {}
likes_given_count = {}

# Iterate over each message object
for message in message_data:
    
    # Skip messages sent by the system
    if message['sender_type'] == 'system':
        continue
    
    # Extract the user ID and name from the message
    user_id = message['user_id']
    user_name = user_id_to_name.get(user_id, user_id)  # Use user ID if name is not found
    
    # Extract the list of user IDs who liked this message
    favorited_by = message.get('favorited_by', [])
    
    # Increment the count of likes for each user, the number of posts by each user,
    # and the total number of likes given by each user
    likes_count[user_id] = likes_count.get(user_id, 0) + len(favorited_by)
    posts_count[user_id] = posts_count.get(user_id, 0) + 1
    for user_id in message['favorited_by']:
        likes_given_count[user_id] = likes_given_count.get(user_id, 0) + 1

# Calculate the total number of likes received by each user
likes_received_count = likes_count

# Calculate the average likes per post for each user
average_likes_per_post = {}
for user_id in likes_count:
    if user_id in posts_count and posts_count[user_id] > 0:
        average_likes_per_post[user_id] = likes_count[user_id] / posts_count[user_id]
    else:
        average_likes_per_post[user_id] = 0

# Replace user IDs with names in the dictionaries
posts_count = {user_id_to_name.get(user_id, user_id): count for user_id, count in posts_count.items()}
likes_given_count = {user_id_to_name.get(user_id, user_id): count for user_id, count in likes_given_count.items()}
likes_received_count = {user_id_to_name.get(user_id, user_id): count for user_id, count in likes_received_count.items()}
average_likes_per_post = {user_id_to_name.get(user_id, user_id): count for user_id, count in average_likes_per_post.items()}

# Sort the dictionaries by values
sorted_posts_count = dict(sorted(posts_count.items(), key=lambda item: item[1]))
sorted_likes_given_count = dict(sorted(likes_given_count.items(), key=lambda item: item[1]))
sorted_likes_received_count = dict(sorted(likes_received_count.items(), key=lambda item: item[1]))
sorted_average_likes_per_post = dict(sorted(average_likes_per_post.items(), key=lambda item: item[1]))


# AVERAGE LIKES PER POST
# Remove users with ratio less than 1
sorted_average_likes_per_post_filtered = {user: avg_likes for user, avg_likes in sorted_average_likes_per_post.items() 
                                          if avg_likes >= 1}

# Plot the bar graph
plt.figure(figsize=(12.5, 8))


# Plot bars
bars = plt.bar(sorted_average_likes_per_post_filtered.keys(), sorted_average_likes_per_post_filtered.values())

# Add labels to bars
def autolabel(bars):
    labeled_heights = {}  # To store labeled heights
    for bar in bars:
        height = bar.get_height()
        rounded_height = round(height, 1)  # Round the height to one decimal place
        if rounded_height not in labeled_heights:  # Check if rounded height has been labeled already
            labeled_heights[rounded_height] = True
            plt.annotate('{:.1f}'.format(height),  
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=4.5
                         )
            print("Label added for height:", rounded_height)
        else:
            print("Skipped label for height:", rounded_height, "as it's already labeled.")
autolabel(bars)
plt.xlabel('Users')
plt.ylabel('Average Number of Likes Per Post')
plt.title('Average Likes Per Post')
plt.xticks(rotation=90, ha='right', fontsize=8)
plt.tight_layout()
plt.show()
