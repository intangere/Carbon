# Carbon
Python-based online BS Card Game back end for the GUI written in App Inventor using Twisted, Flask, and Orbit for exchanging data
Final Game Design Project<br>
Design:<br>
(Original)
-Create sessions with random IDS and store them on the device<br>
-Join sessions by sending friends random ID from device<br>
-Auto align cards<br>
-Move cards and build pile in the center<br>
-5 second interval refresh rate<br>
-8bit style cards<br>
Final version:<br>
-No card pile in the center due to tiem constraints<br>
-Users must pick IDS instead of them randomly generating<br><br>
Features
<hr>
-Four player minimum requirement per game<br>
-Duplicate usernames are not allowed<br>
-Duplicate game ID's are not allowed<br>
-Supports hands up to 25 card hands, Upon having 25 cards a message pops up recommending you uninstall this as you are terrible at it<br>
-Blocks hackers for the most part<br>
-BS button is functional<br>
-Playing cards is functional<br>
-Turns are implemented<br>
-Game over may work, unconfirmed (Didn't have time to simulate an entire game)<br>
-Offline sessions, you can join a game any time and continue it<br><br>

Todo<br>
-Implement ai based games prefixed with ai_gameID<br>
-Implement card animation so players see the pile in the middle of the game<br>
