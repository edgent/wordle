'''
To do:
- work out how to avoid clearing inputs after submission
- reset URL after submission? or use URL to populate inputs, and add a "reset" button
- build 'yellow position history' functionality
- add caveats to page about what won't work (e.g. yellow position history, list includes some names)
- return how many options the user has
- return more than just 1 options / give some choice
- update Guesser to be more intelligent (like autoplay is)
'''

from flask import Flask
from flask import request, escape
import guesser

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
    yellow_letters = str(escape(request.args.get('yellow_letters_input','')))
    grey_letters = str(escape(request.args.get('grey_letters_input','')))
    
    # updating the manual_game dictionary used in the guessing functions
    for i in range(5):
      manual_game['green'][i] = str(escape(request.args.get(('green'+str(i+1)),'')))

    manual_game['yellow'] = set(yellow_letters)
    manual_game['grey'] = set(grey_letters)

    # using the Guesser object to return a guess
    guess_output = bot.generate_guess(manual_game,method='letter_frequency',sample_n=5)
    text_to_return = f'Our best guess for the answer is <b>{guess_output}</b>'

    return ('''
    <form method= "get" action = "" enctype="application/x-www-form-urlencoded">
                  <div class = "form_title">
                    <u>Enter the letters you have so far and hit submit to get our best guess for the next word</u>
                  </div><br>
                  
                  <div class = "yellow_letters">
                    <p>Type in any yellow letters you currently have (no commas or spaces)</p>
                    <input type="text" name = "yellow_letters_input" enctype="application/x-www-form-urlencoded">
                  </div>
                  
                  <div class = "grey_letters">
                    <p>Type in any grey letters you currently have (no commas or spaces)</p>
                    <input type="text" name = "grey_letters_input" enctype="application/x-www-form-urlencoded">
                  </div>

                  <table class="green_letters">
                    <p>Type in any green letters you currently have (must be in the right boxes, 1 per box)</p>
                    <td><input type="text" name = "green1"></td>
                    <td><input type="text" name = 'green2'></td>
                    <td><input type="text" name = "green3"></td>
                    <td><input type="text" name = "green4"></td>
                    <td><input type="text" name = "green5"></td>
                  </table>
                  
                  <div class = "submit_button">
                    <br>
                    <input type="submit" name="submit_form" enctype="application/x-www-form-urlencoded">
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