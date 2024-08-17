This is code to provide both basic and a more in depth data visualization from a GroupMe export. Likes being the most explored variable. 

How to run it (instructions for a 5th grader):

Step 1 : Groupme Export

   a - Log into your GroupMe on a computer
   
   b - Go to your profile and scroll down to the bottom
   
   c - Click "Export my data" button
   
   d - Click "Create Export"
   
   e - ONLY click the "Message Data" box, nothing else matters
   
   f - Click "Next"
   
   g - Click the box for the ONE conversation you want to export. 
   
   h - Click "Next" and wait for your export to be generated, click back and it should be there
   
   i - Click the blue link "Download 1 of 1"
   
   j - Unzip that folder and try to remember where you put it!
   

Step 2 : Using 

    a - Clone the repo and get the few dependencies needed (sry to the 5th grader, i got lazy)
    
    b - Run main.py
    
    c - A 90s lookin window should pop open
    
    d - Click "Browse" and select the your unzipped folder. It will probably be named something like 00001 or 894124718
    
    e - Select which of the plots you want. Read more below to see what each of the 3 is, or just run it and see for yourself.
    


What each plot does:

allEncompassingPlot.py:
Plots a single very data filled, comprehensive color coated bar graph with additional boxes of top user stats and 'GOAT' conversation for the 3 users with the best overall stats. Also, saves the png for you.

avgLikesPerPostPlot.py
Surprise surprise... it just plots average likes per post.

fiveSpecificStats.py:
Will plot 5 separate bar graphs, each opening after the previous is closed.
- Number of posts 
- Number of likes given
- Number of likes received
- avg likes/post for infrequent posters (<10 posts)
- avg likes/post for frequent posters (>10 posts)

I just added the folder: 'Example Plots' to provide examples of each kind of plot.

This project definitely could be improved in a few areas: 
- Using kernels for individual plots so you dont deal with multiple plots every time you run
- I had to manually input some IDs that for some reason weren't recognized
- I manually chose GOAT contenders, could have some equation to quantitatively figure that out
- Using more advanced plots to include more data in a more visually aesthetic way
- Make allEncompassingPlot plot more understandable. It makes sense, just kind of hard to follow for first time viewers, mostly to do with the top 10% situation.
