## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

# Worked with Sindu Giri
# Used iTunes API documentation: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import requests
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def welcome_to_SI364():
    return 'Welcome to SI 364!'

@app.route('/movie/<movie_name>')
def movie(movie_name):
    params = {
        "term":     movie_name,
        "entity":   "movie"
    }
    baseurl = "https://itunes.apple.com/search"
    response = requests.get(baseurl, params = params)
    
    return str(response.text)






## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!




## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.
@app.route('/question')
def question():
    html = """
    <form method="POST" action="/square">
        <label>Enter the number you want to square:<br></label>
        <input type="num" required placeholder="your favorite number" name="number">
        <button type="submit">Submit</button>
    </form>
    """
    return html

@app.route('/square', methods = ['GET', 'POST'])
def square():
    number = int(request.form.get("number", "got nothing"))
    return "Double your favorite number is {}".format(str(number*number))




## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.


@app.route('/problem4form', methods = ['GET', 'POST'])
def creator():
    print(request.method)
    # form to select the title
    form = """
    <h3>Find the creator of your favorite work of art:</h3>

    <form method="POST" action="/problem4form">
        <label><b>Enter a title:</b><br></label>
        <input type="text" required placeholder="song, movie or book" name="title">
        
        <br>
        <br>
        <b>Where would you like to search?</b>
        <br>
        <input type="radio" name="entity" value="movie" checked />
        <label for="movie">Movie</label>
        <input type="radio" name="entity" value="music" />
        <label for="song">Song</label>
        <input type="radio" name="entity" value="ebook" />
        <label for="book">Book</label>
        <br>        <br>

        <button type="submit"><b>Submit</b></button>
    </form>
    """

    # if user already submitted the form, send request to the API
    if request.method == "POST":
        try:
            # get the title from POST
            title = request.form.get("title")

            # get the checkboxes from POST
            params = dict(term = title, media = request.form.get("entity"))


            # make a request to the API with params
            baseurl = "https://itunes.apple.com/search"
            response = requests.get(baseurl, params = params).json()

            # find the right data in the JSON
            author = response["results"][0]["artistName"]
            track_name = response["results"][0]["trackName"]

            author_text = "\"{}\" is by:<br> <b>{}</b>".format(track_name, author) 
            return form + author_text
        except:
            return form + "Can't find anything like this! 😱 "
    else:
        return form



if __name__ == '__main__':
    app.run()