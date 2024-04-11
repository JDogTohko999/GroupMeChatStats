This is code to provide both basic and a more in depth data visualization from a GroupMe export. Likes being the most explored variable. 

What each file does:

allEncompassingPlot.py:
Plots a single very data filled, comprehensive color coated bar graph with additional boxes of top user stats and 'GOAT' conversation for the 3 users with the best overall stats. 

specificStats.py:
Will plot 5 separate graphs, all sorted from low -> high, left -> right:
- Number of posts 
- Number of likes given
- Number of likes received
- avg likes/post for infrequent posters (<10 posts)
- avg likes/post for frequent posters (>10 posts).
  
The other files are unimportant, but I just didn't feel the need to delete them, maybe they're useful in some way. 
avgLikesPerPost plots... surprise surprise: avg likes per post.
Names 2IDs prints names and their IDs. 
sandBox was just for me to play around with things.
usingConv&Every was my first attempt at cleaning the data with the conversation.json and everybody.json files that the groupme export provides. The data was easier to clean in those jsons, but it was insufficient. allEncompassingPlot uses message.json which proved to be way better despite being harder to clean.

I just added the folder: 'Plot Gallery' to provide examples of each kind of plot.

This project definitely could be improved in a few areas: 
- Using kernels for individual plots so you dont deal with multiple plots every time you run
- I had to manually input some IDs that for some reason weren't recognized
- I manually chose GOAT contenders, could have some equation to quantitatively figure that out
- Using more advanced plots to include more data in a more visually aesthetic way
- Make allEncompassingPlot plot more understandable. It makes sense, just kind of hard to follow for first time viewers, mostly to do with the top 10% situation.
