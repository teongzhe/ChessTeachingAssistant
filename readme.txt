This software is developed as an aid for (passionate) chess teachers.
The idea originated from Chua Thean Cheang, with a request for a piece of software which enabled the user to freely specify the position of pieces on the chess board to enable education of how to handle specific situations.
Functions that are currently implemented include:
1. Playing a normal Chess or Xiangqi Game (no AI is included so it must be player-vs-player).
2. Clearing off the whole board and specifying the position of pieces using the panel on the left hand side. This is useful for end-game demonstrations.
3. Taking back moves and undoing take backs.
4. Quick save and load functions to memorize and load the current state (does not save the move list meaning no take backs will be permitted after loading)
5. Saving and loading positions from files




The main function is located in "chess_teaching_assistant.py".
The program can be started by running "python3 chess_teaching_assistant.py" in the console.
Note that the program is tested in python3. It may be necessary to change some import filenames when running using python2.

As this project was developed in a rush, many functions vital for debugging (mainly the throwing and catching of exceptions) are left out. Bugs are currently only fixed when a bug report is filed directly to me.

Furthermore, development was not carried out with scalability in mind. Instead, a waterfall approach is used, as opposed to scrum which is fairly popular nowadays, for the reason that there is not much time to organize the code for scalability and a working edition is required in as short a time period as possible. However, I plan to refactor the code for scalability in the future, either in my free time or when there are requests to add new functionalities to the existing code.
