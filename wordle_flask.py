# developed using this guide https://realpython.com/python-web-applications/#escape-user-input
# deployed using this guide https://realpython.com/flask-by-example-part-1-project-setup/

'''
To do:
- validate input (1 character, lower case)
- work out how to avoid clearing inputs after submission
- reset URL after submission? or use URL to populate inputs, and add a "reset" button
- add caveats to page about what won't work (e.g. yellow position history, list includes some names)
- return how many options the user has
- return more than just 1 options / give some choice
- update Guesser to be more intelligent (like autoplay is)
- work out how to store HTML in a standalone file, and have a CSS sheet
- work out how to re-create the wordle grid - click tiles to get them to change colour/state and feed that information back to the programme 
- give different output options: single guess, how many options there are, word endings that work, top 5 common words that fit
'''

from flask import Flask
from flask import request, escape
import guesser
import pandas as pd 

bot = guesser.Guesser() # instantiating a Guesser object that will makea  smart guess from the user input


app = Flask(__name__)

@app.route('/')
def index():
    # dictionary used in wordle guessing functions
    manual_game = {
      'green': {0: '', 1: '', 2: '', 3: '', 4: ''}, 
      'yellow': set(''), 
      'yellow_position_history': {0:[''],1:[''],2:[''],3:[''],4:['']}, 
      'grey': set('')
    }
    # extracting letters from the HTTP request
    yellow_letters = str(escape(request.args.get('yellow_letters_input',''))).lower()
    grey_letters = str(escape(request.args.get('grey_letters_input',''))).lower()
    
    # updating the manual_game dictionary used in the guessing functions
    for i in range(5):
      manual_game['green'][i] = str(escape(request.args.get(('green'+str(i+1)),''))).lower()

    for i in range(5):
      manual_game['yellow_position_history'][i] = str(escape(request.args.get(('yellow'+str(i+1)),''))).lower()

    manual_game['yellow'] = set(yellow_letters)
    manual_game['grey'] = set(grey_letters)

    # using the Guesser object to return a guess
    guess_output = bot.generate_guess(manual_game,method='letter_frequency',sample_n=1)
    options = bot.generate_enriched_options(manual_game)
    number_of_options = len(options)
    top_5_options = str(list(options.sort_values(by='word_frequency_rank',ascending=False)[:5].index)).replace("'",'').replace('[','').replace(']','')
    # text_to_return = f'Our best guess for the answer is <b>{guess_output}</b>'
    text_to_return = f"""
      We think there are {number_of_options} possible options. \n
      The word with the most informational value is {guess_output}.\n
      The most 5 common possible words (most popular first) are: {top_5_options}.\n
      Good luck!
      """

    return ('''
    <form method= "get" action = "" enctype="application/x-www-form-urlencoded">
                  <div class = "form_title">
                    <u>Follow the steps below to find out what the best options are in your game of Wordle. Repeat until done!</u>
                  </div><br>
                  
                  <div class = "yellow_letters">
                    <p>1. Type in any letters which are <b>currently</b> yellow (no commas or spaces) - <b>you will need to update this when you find the position that changes them to green.</b></p>
                    <input type="text" name = "yellow_letters_input" enctype="application/x-www-form-urlencoded" style="background-color: #FFFF00">
                  </div>

                  <table class="yellow_position_history">
                    <p>
                      2. For each letter position (1 - 5) enter any letters that have <b>ever</b> been yellow in that position (no commas or spaces, no need to repeat letters).<br>
                      <em>e.g. If your first guess was 'bread' and your second was 'trade', and you got yellows for the first letter each time, enter "bt" in the "Position 1" box below.</em> 
                    </p>
                    <td><input type="text" name = "yellow1" placeholder="Position 1" style="background-color: #FFFF00"></td>
                    <td><input type="text" name = 'yellow2' placeholder="Position 2" style="background-color: #FFFF00"></td>
                    <td><input type="text" name = "yellow3" placeholder="Position 3" style="background-color: #FFFF00"></td>
                    <td><input type="text" name = "yellow4" placeholder="Position 4" style="background-color: #FFFF00"></td>
                    <td><input type="text" name = "yellow5" placeholder="Position 5" style="background-color: #FFFF00"></td>
                  </table>
                  
                  <div class = "grey_letters">
                    <p>3. Enter all grey letters you have so far (no commas or spaces)</p>
                    <input type="text" name = "grey_letters_input" enctype="application/x-www-form-urlencoded" style="background-color: #E6E6E6">
                  </div>

                  <table class="green_letters">
                    <p>4. Enter all green letters you have so far (must be in the right boxes, 1 per box)</p>
                    <td><input type="text" name = "green1" placeholder="Position 1" style="background-color: #2ECE2B"></td>
                    <td><input type="text" name = 'green2' placeholder="Position 2" style="background-color: #2ECE2B"></td>
                    <td><input type="text" name = "green3" placeholder="Position 3" style="background-color: #2ECE2B"></td>
                    <td><input type="text" name = "green4" placeholder="Position 4" style="background-color: #2ECE2B"></td>
                    <td><input type="text" name = "green5" placeholder="Position 5" style="background-color: #2ECE2B"></td>
                  </table>
                  
                  <div class = "submit_button">
                    <br>
                    <br>
                    <br>
                    <input type="submit" name="submit_form" enctype="application/x-www-form-urlencoded" style="height:40px; width:120px; font-weight:bold">
                    <br>
                  </div>
              </form>
    ''' + text_to_return
    )

# @app.route("/")
# def index():
#     yellow_letters = request.args.get("yellow_letters_input", "")
#     return (yellow_letters)

# @app.route("/<int:celsius>")
# def fahrenheit_from(celsius):
#     """Convert Celsius to Fahrenheit degrees."""
#     fahrenheit = float(celsius) * 9 / 5 + 32
#     fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
#     return str(fahrenheit)

if __name__ == "__main__":
    app.run(debug=True)