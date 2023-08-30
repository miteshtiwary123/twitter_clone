# twitter_clone
In this project i am building twitter clone <br>
Firstly i have setup the environment for my project and created some basic templates and added navbar using bootstrap. <br>
Then i created superuser and make some changes in admin fields, I added Profile model and inline this profile model into user model. <br>
Then i use django signals post_save module to create profile page automatically when user is created and also added automatic follow to themselves. <br>
Then i have created frontend for profile_list and uses bootstrap card to show all the profile exclude current user also added static folder to store images and also check if user is login then see profile_list otherwise redirect to home page and show message. <br>
Then created a profile page for the user who logged in and also added follower and followed by section in the profile page. also created clickable @username.
