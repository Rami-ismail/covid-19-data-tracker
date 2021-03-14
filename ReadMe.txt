========================================================================
    	     Welcome to the
         Corona Virus Data Tracker V1.0
	       ReadMe File
	      May 19, 2020
========================================================================
installation guide : extract the zip file in a folder make sure all the other folders are present.
the actual code is called covid-19.py just double click on it andd it should run perfectly
other than the code there should be 3 folders and an icon.
accounts folder :stores the data bases also contain a pre-made file "zouzou.db"
texture folder: contains all the images and the dependencies of the code.  
an icon" coronavirus.ico file
video folder: contains the 2 videos of the technical and the client presentation

========================================================================
0. CONTENTS
========================================================================
1. Installing Required Libraries
2. User Guide
3. Known Issues
4. Future Additions
5. Changelog
6. Refrences and API's
========================================================================
========================================================================
1. Installing Required Libraries
========================================================================

WINDOWS : Press windows + R. Type in cmd and press enter
MAC OS  : Press command (⌘) + Space Bar to open Spotlight search. Type in Terminal and press enter.

Use the next set of commands to install NumPy and Pillow

python -m pip install requests
python -m pip install pillow
python -m pip install smtplib
python -m pip install matplotlib
python -m pip install sqlite3

========================================================================
2. User Guide
========================================================================
-You need to register an account first: type in your name and email then choose a username and a password to access the app,your credantials are saved in a table of a "username.db" file
   PS: the "username.db" contains also a table for storing data
-login with your username and password
-pick a country in the combobox to request the corona virus data for the selected country with a pie chart
-the data can be analysed,shared,saved and displayed or cleared
-to analyse the data click on the analyse button:
   *you can choose to analyse your current data(displays a bar chart of the displayed statistics)
   *you can choose to analyse saved data (displays an plot that describes the evolution of a chosen statistic day by day or total statistics)
    PS: you have to save 2 distinct data values for a specific country wich you select from the combobox in order to visualize the evolution plot
-to share the data you can click on the share button to share via email the gathered data
-to save the data you can click on the save button (the data will be saved in a Table in the data base file)
-to display data you can click on the history button wich will diplay labels containing the data saved in the database 
-press on the clear button to reactivate the combobox in order to select another contry to display it's data
-to clear your database press on the clear button in the history gui
-Q&A section is now available:These are the most commonly Frequently Asked Questions and Answers about the Corona virus.
-you can logout of your account using the logout button on the top right of the screen


**PS: there is an account called zouzou that contains pre-saved data for you to visualize the evolution plot (don't forget to select lebanon):
      username=zouzou
      password=123
========================================================================
3. Know Issues
========================================================================
-the save button can save duplicated data(but only the distinct value are shown in the history)
-the history gui must be closed and reopenned to be refreshed 
-Disclaimer: this app hasn't been updated since 2020	
========================================================================
4. Future Additions
========================================================================
========================================================================
5. Changelog
========================================================================

N/A

=========================================================================
6.Refrences and API's
=========================================================================
https://corona.lmao.ninja