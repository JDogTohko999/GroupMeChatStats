import json

# Load JSON data about the group members
with open('C:\\Users\\jdog1\\OneDrive\\Documents\\Spring2024\\Data Science Projects\\Delta Quotes Analysis\\Exported GM chat Data\\conversation.json', 'r', encoding='utf-8') as file:
    group_data = json.load(file)

# Print names and their respective IDs
for member in group_data['members']:
    user_id = member['user_id']
    user_name = member.get('name', 'Unknown')  # Use 'Unknown' if name is not found
    print(f"Name: {user_name}, ID: {user_id}")
