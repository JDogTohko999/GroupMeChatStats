import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

# Load JSON data about the group members
with open('FILE PATH OF conversation.json', 'r', encoding='utf-8') as file:
    group_data = json.load(file)

# Create a mapping from user IDs to names
user_id_to_name = {member['user_id']: member['name'] for member in group_data['members']}

# Manually add missing user IDs and names to the user_id_to_name dictionary
user_id_to_name.update({
    '12345678': 'John Doe', #example
    '23456789': 'Average Joe', #example2
})

# Load JSON data from message.json
with open('FILE PATH OF message.json', 'r', encoding='utf-8') as file:
    message_data = json.load(file)

# Initialize dictionaries
likes_count = {}
posts_count = {}
likes_given_count = {}
max_likes_received_per_user = {}

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

    # Update max_likes_received_per_user if the current message has more likes than previous messages for the user
    max_likes_received_per_user[user_id] = max(max_likes_received_per_user.get(user_id, 0), len(favorited_by))

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
sorted_max_likes = dict(sorted(max_likes_received_per_user.items(), key=lambda item: item[1], reverse=True))
sorted_posts_count = dict(sorted(posts_count.items(), key=lambda item: item[1]))
sorted_likes_given_count = dict(sorted(likes_given_count.items(), key=lambda item: item[1]))
sorted_likes_received_count = dict(sorted(likes_received_count.items(), key=lambda item: item[1]))
sorted_average_likes_per_post = dict(sorted(average_likes_per_post.items(), key=lambda item: item[1]))

# Remove users with ratio less than 1
sorted_average_likes_per_post_filtered = {user: avg_likes for user, avg_likes in sorted_average_likes_per_post.items() if avg_likes >= 1}

# Define a colormap for lower 90% of users
min_posts_90 = min(sorted_posts_count.values())  # Minimum value for the lower 90%
max_posts_90 = np.percentile(list(sorted_posts_count.values()), 90)  # 90th percentile for the lower 90%
norm_90 = mcolors.Normalize(vmin=min_posts_90, vmax=max_posts_90)
cmap_90 = plt.cm.get_cmap('viridis_r', lut=None)

# Plot the bar graph
plt.figure(figsize=(13, 7))

# Plot bars with colors based on total number of posts for the lower 90%
bars = []
for user, posts in sorted_average_likes_per_post_filtered.items():
    if sorted_posts_count[user] <= max_posts_90:
        color = cmap_90(norm_90(sorted_posts_count[user]))  # Use the normalized value for the lower 90%
    else:
        color = 'black'  # Assign a distinct color for top 10% of users
    bars.append(plt.bar(user, posts, color=color))

# Create a colorbar for the lower 90%
sm = plt.cm.ScalarMappable(cmap=cmap_90, norm=norm_90)
sm.set_array([])
plt.colorbar(sm, ax=plt.gca(), label='Number of Posts (excluding top 10%)')

# Identify top 10% users by total number of posts
top_users = {user: posts_count[user] for user in sorted_posts_count if posts_count[user] > max_posts_90}

# Sort the top users by number of posts
sorted_top_users = dict(sorted(top_users.items(), key=lambda item: item[1], reverse=True))

# Calculate average likes per post for the top users
average_likes_per_post_top_users = {user: average_likes_per_post[user] for user in sorted_top_users}

# Sort the top users by average likes per post
sorted_top_users_by_likes = dict(sorted(average_likes_per_post_top_users.items(), key=lambda item: item[1], reverse=True))

# Prepare the text for the box including average likes per post and ranking
box_text = "Top 10% in Posts (black in graph)\n\n"
rank = 1
for user, likes_per_post in sorted_top_users_by_likes.items():
    posts = sorted_top_users[user]
    likes_received = likes_received_count[user]
    box_text += f"{rank}. {user}: {likes_received}/{posts} (likes/posts) : {likes_per_post:.2f}\n"
    rank += 1

# Prepare the text for the box including top 5 users in terms of likes given
top_5_likes_given = sorted(likes_given_count.items(), key=lambda x: x[1], reverse=True)[:9]
box_text_top_5_likes_given = "Top 10%  in Likes Given:\n\n"
for rank, (user, likes_given) in enumerate(top_5_likes_given, start=1):
    box_text_top_5_likes_given += f"{rank}. {user}: {likes_given} likes given\n"

# Prepare the text for the box including top 5 quotes (most liked) and their users
top_5_quotes = list(sorted_max_likes.items())[:9]
box_text_top_5_quotes = "Top 5 Most Liked Quotes:\n\n"
for rank, (user_id, max_likes) in enumerate(top_5_quotes, start=1):
    user_name = user_id_to_name.get(user_id, user_id)
    box_text_top_5_quotes += f"{rank}. {user_name}, {max_likes} likes: \n"


# Initialize dictionaries to store new metrics
top_10_likes_sum = {}

# Iterate over each user
for user_id in user_id_to_name.keys():
    user_name = user_id_to_name[user_id]
    
    # Get all messages sent by the user (excluding system messages)
    user_messages = [message for message in message_data if message['user_id'] == user_id and message['sender_type'] != 'system']
    # Sort the messages based on the number of likes
    sorted_messages = sorted(user_messages, key=lambda x: len(x.get('favorited_by', [])), reverse=True)
    # Sum up the likes for the top 10 posts  
    top_10_likes_sum[user_name] = sum(len(message.get('favorited_by', [])) for message in sorted_messages[:10])

#GOAT
# Define the user IDs of the selected users. Manually select the top three, or however many you want, you think deserve to be in the GOAT conversation
selected_users = ['12345678', '23456789', '34567891']

# Initialize the GOAT box text
goat_box_text = "Delta Quotes GOATs\n\n"

# Iterate over each selected user
for rank, user_id in enumerate(selected_users, start=1):
    user_name = user_id_to_name.get(user_id, user_id)
    
    # Total number of posts
    total_posts = posts_count[user_name] if user_name in posts_count else 0
    
    # Total number of received likes
    total_likes_received = likes_received_count[user_name] if user_name in likes_received_count else 0
    
    # Average likes per post
    avg_likes_per_post = average_likes_per_post[user_name] if user_name in average_likes_per_post else 0
    
    # Total number of likes given
    total_likes_given = likes_given_count[user_name] if user_name in likes_given_count else 0
    
    # Likes from top 10 posts
    top_10_likes = top_10_likes_sum[user_name] if user_name in top_10_likes_sum else 0
        
    # Get the number of likes on each of their best 5 posts
    user_best_posts_likes = []
    user_messages = [message for message in message_data if message['user_id'] == user_id and message['sender_type'] != 'system']
    user_best_posts = sorted(user_messages, key=lambda x: len(x.get('favorited_by', [])), reverse=True)[:3]
    for post in user_best_posts:
        user_best_posts_likes.append(len(post.get('favorited_by', [])))

    # Add user metrics to the GOAT box text
    goat_box_text += f"{rank}. {user_name}:\n"
    goat_box_text += f"   Likes: {total_likes_received}\n"
    goat_box_text += f"   Posts: {total_posts}\n"
    goat_box_text += f"   Avg: {avg_likes_per_post:.2f}\n"
    goat_box_text += f"   Likes Given: {total_likes_given}\n"
    goat_box_text += f"   Top 3 Posts: {', '.join(map(str, user_best_posts_likes))}\n"
    goat_box_text += f"   Top 10 Posts Sum: {top_10_likes}\n\n"
goat_box_text += "NBA Most Similar Goats:\n"  #Used chatGPT to list a few similar NBA Goats and I chose from there
goat_box_text += "1. Lebron \n"
goat_box_text += "2. Jordan \n"
goat_box_text += "3. Kareem \n"

# Add the box with text to the plot
plt.text(0.05, 0.95, box_text, transform=plt.gca().transAxes, fontsize=6,
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

plt.text(.29, 0.95, box_text_top_5_likes_given, transform=plt.gca().transAxes, fontsize=6, 
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

# Add the box with text for top 5 quotes to the plot
plt.text(0.48, .95, box_text_top_5_quotes, transform=plt.gca().transAxes, fontsize=6, 
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

# Add the GOAT conversation box to the plot
plt.text(0.05, .7, goat_box_text, transform=plt.gca().transAxes, fontsize=5.6, 
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

# Add labels to bars
def autolabel(bars):
    labeled_heights = {}  # To store labeled heights
    for bar in bars:
        for rect in bar:
            height = rect.get_height()
            rounded_height = round(height, 1)  # Round the height to one decimal place
            if rounded_height not in labeled_heights:  # Check if rounded height has been labeled already
                labeled_heights[rounded_height] = True
                plt.annotate('{:.1f}'.format(height),  
                             xy=(rect.get_x() + rect.get_width() / 2, height),
                             xytext=(0, 3),  # 3 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom', fontsize=4.1
                             )
autolabel(bars)
plt.xlabel('Users')
plt.ylabel('Average Number of Likes Per Post')
plt.title('Delta Quotes Analysis')
plt.ylim(3.5, None) # Set the lower limit of the vertical axis
plt.xticks(ticks=np.arange(len(sorted_average_likes_per_post_filtered)), labels=sorted_average_likes_per_post_filtered.keys(), rotation=90, ha='center', fontsize=7.3)
plt.tight_layout()
plt.savefig('DeltaQuotesVisualized.png', dpi=300)  
plt.show()



"""
# Print the top 5 users' most liked posts and the user who posted them
print("Top 5 Users' Most Liked Posts:")
for rank, (user_id, max_likes) in enumerate(sorted_max_likes.items(), start=1):
    if rank > 40:
        break
    user_name = user_id_to_name.get(user_id, user_id)
    print(f"{rank}. User: {user_name}, Number of Likes: {max_likes}")
    """
