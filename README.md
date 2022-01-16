# Chess Teaching Assistant - Overview
This software is developed as an aid for chess teachers.
The idea originated from Chua Thean Cheang, with a request for a piece of software which enabled the user to freely specify the position of pieces on the chess board to enable education of how to handle specific situations.
Functions that are currently implemented include:
1. Playing a normal Chess or Xiangqi Game (no AI is included so it must be player-vs-player).
2. Clearing off the whole board and customization of the position of chess pieces. This is useful for end-game demonstrations.
3. Taking back moves and undoing take backs.
4. Quick save and load functions to memorize and load the current state (does not save the move list meaning no take backs will be permitted directly after loading)
5. Saving and loading positions of pieces from files (also does not save the move list)



# Getting started
Follow the instructions below to get started!
1. Download the zip package from https://drive.google.com/uc?id=1gI1Pe5u1tDIbaU6Vg2gpoLkuFNjr16UZ&export=download
2. Unzip the package to a location of your choice
3. Check that the contents include `ChessTeachingAssistant.exe` and a folder named `img` (don't delete this folder!)
3. Run `ChessTeachingAssistant.exe`
4. Start teaching!

Well.... That's it if you didn't run into any problems.  
The uploaded `ChessTeachingAssistant.exe` only works on computers with similar operating systems to the computer on which it was built on.
If you encounter problems when running `ChessTeachingAssistant.exe`, do read on, and maybe get your IT consultant to help you out if you're feeling lost!



# For the more tech savvy... (seriously)
This section is only necessary if you ran into any errors while following the instructions under the previous section.  
Note that the instructions here may be hard to follow for non-IT oriented people, so try to get your school ICT teacher to help you out!

## 1. Getting ready
### 1.1 Install python
First step will be to install python, preferably version 3.9.4 since this is the version I am using.
You can download and install from https://www.python.org/downloads/release/python-394/
### 1.2 Just in case, try to install tkinter
Open command prompt and run `pip install tk`.  
Some versions of python already come with tkinter pre-installed so this may not be a necessary step.
*I think* python version 3.9.4 already comes with tkinter pre-installed.
### 1.3 Git
If you choose to download directly from https://github.com/teongzhe/ChessTeachingAssistant then this piece of software is not necessary.
However, this software does make it easier to update applications as you don't have to download the whole zip package, only the updated portions. If you choose not to download, follow `Method 1` in the following section and if you choose to download, follow `Method 2`.

If you don't think you're tech savvy I definitely recommend *not* downloading this!


## 2. Updating the package
### Method 1: Download the package and unzip
1. Download the zip package from https://github.com/teongzhe/ChessTeachingAssistant by clicking on the `Code` button and selecting `Download ZIP`
2. Unzip to the location of your choice (don't overwrite your old directory just yet!)
3. Open command prompt and `cd` to the newly downloaded directory with `Main.py` (this is the file we will be building in the next step)
4. `python Main.py`
5. The application should launch, if not, do drop me an email at teongzhechua@gmail.com

### Method 2: Update using git
1. Open command prompt and `cd` to your `ChessTeachingAssistant` directory.
2. `git checkout master`
3. `git pull`
4. `python Main.py`
5. The application should launch, if not, do drop me an email at teongzhechua@gmail.com



## 3. Building the application (optional)
This is only if you want to build and share `ChessTeachingAssistant.exe` to others to save them the trouble you have had to go through. It is a good deed indeed.
1. Download `pyinstaller` by running `pip install pyinstaller` in your command prompt. You only have to do this the first time, subsequent buildings do not require this step!
2. Open command prompt and `cd` to your `ChessTeachingAssistant` directory (try to make sure that you have the latest version)
3. `pyinstaller --onefile -w Main.py -n ChessTeachingAssistant`
4. Copy `dist\ChessTeachingAssistant.exe` to the main directory, i.e. directly under the `ChessTeachingAssistant` folder




# A few final notes
As this project was developed in a rush, some parts of the project may be bugged.
If it doesn't run properly do report the issue to me at teongzhechua@gmail.com, preferably with a screenshot of the error message (if any) and a detail of what you were attempting to do when the error occured!
I will be adding additional error messages for debugging over time, so that you can report bugs more easily.

Also, while there may still be bugs here and there, do not hesitate to share this piece of software with your friends or family or any of your acquaintances!
When sharing, do remember to share the link for github: https://github.com/teongzhe/ChessTeachingAssistant so that they can keep their copy updated as well!
