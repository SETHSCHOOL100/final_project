import os

from flask import Flask, session
from flask import Flask, render_template, request
from flask_session import Session
import random

#######################################################################
#App configurations
#######################################################################
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    Session(app)
    app.config['SESSION_TYPE'] = 'filesystem'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
#######################################################################
#App configurations ended
#######################################################################


#######################################################################
#Classic Mode
####################################################################
    #Home Page
    @app.route('/')
    def index():
        session['score'] = 0
        #First Question

        return render_template('index.html')


    @app.route("/Welcome_Labyrinth",methods=['GET', 'POST'])
    def Welcome_Labyrinth():
        
        return render_template('Welcome_Labyrinth.html')
        
    #######################################################################
    #This function is the way you will change your score
    #The texts are going to be the text that will be shown in the next screen
    def button_clicking(intro_text, a_text,b_text,c_text, print_message_for_debug):
        print("##################################")
        if request.method == "POST":
            print("You sent a post request")
   
            if request.form.get("submit_a"):
                session['score'] = session['score']+random.randint(-5, 15)
                print('User should have selected a')

            elif request.form.get("submit_b"):
                session['score'] = session['score']+random.randint(-5, 15)
                print('User should have selected b')

            elif request.form.get("submit_c"):
                session['score'] = session['score']+random.randint(-5, 15)
                print('User should have selected c')

            elif request.form.get("submit_d"):
                session['score'] = session['score']+random.randint(-5, 15)
                print('User should have selected d')

            else:
                print("MAJOR ISSUE!! User choice was neither a,b,c, or d")
                pass

            session['intro_text'] = intro_text
            session['choice_a_text'] = a_text
            session['choice_b_text'] = b_text
            session['choice_c_text'] = c_text
            session['choice_d_text'] = d_text
            print('message: ', print_message_for_debug)
            print('new score: ', session['score'])
            
        else:
            print("MAJOR ERROR IN BUTTON CLICK FUNCTION IF NOT GOING INTO THE FIRST ROUND")
            print("If you did get this message you sent a get request instead of a post request")
        print("##################################")


    #######################################################################
    #1st Question function
    @app.route("/classic_mode_q1",methods=['GET', 'POST'])
    def first_question():
        session['intro_text'] = "You fell asleep in the library and you suddenly find yourself late to Miss Misa's class! What are you going to do!?"
        session['choice_a_text'] = 'Start running to class'
        session['choice_b_text'] = 'Keep sleeping'
        session['choice_c_text'] = 'Roam the hallway'
        message = 'Classic Mode was selected'
        next_page = '/classic_mode_q2'

        button_clicking(session['intro_text'], session['choice_a_text'], session['choice_b_text'], session['choice_c_text'], message)
        
        return render_template('classic_mode.html', intro = session['intro_text'], a_text = session['choice_a_text'], b_text = session['choice_b_text'], c_text = session['choice_c_text'], pg_u_goto_after_clicked = next_page) 
    #######################################################################
    #Classic Mode End Screen
    @app.route("/end_screen/", methods=['POST'])
    def ending():
        button_clicking('', '', '', '', 'Answered Q5 and below will be the final score')  
        score = session['score']
        print('Final score: ', score)
        if score < 6:
            last_scene = render_template('end_screen.html', ending_text = 'Sorry, you got in trouble anyway...')
        elif score == 7 or score == 9 or score == 11:
            last_scene = render_template('end_screen.html', ending_text = 'I have no idea but you escaped!!!!')
        else:
            last_scene = render_template('end_screen.html', ending_text = "Uhhh.. You just got yourself suspended...")

        print("##################################")
        return last_scene
#######################################################################
#Classic mode ended
#######################################################################
    @app.route("/traps",methods=['GET', 'POST'])
    def traps():
        print("")
        return render_template('Traps_Monsters.html')


#######################################################################
#Create session & run the application
    sess = Session()
    sess.init_app(app)

    return app








#helpful websites
#https://stackoverflow.com/questions/15557392/how-do-i-display-images-from-google-drive-on-a-website
#https://unsplash.com/images/stock/blogging
#https://getbootstrap.com/docs/3.3/components/#btn-groups
#https://www.w3schools.com/bootstrap/bootstrap_theme_me.asp
#https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event