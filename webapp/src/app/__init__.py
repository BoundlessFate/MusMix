# DOES NOT UTILIZE THIS FILE- MAY DELETE AFTERWARDS
# run 'ng serve' in directory

from flask import Flask, jsonify

app = Flask(__name__)

# If using "/search" after URL as song search site
# Run get_data() in console

@app.route('/', methods=['GET'])
def index():
    return render_template('mainPage.html')

@app.route('/searchPage', methods=['GET'])
def search():
    return render_template('searchPage.html', username="FOUND FROM FLASK")


#if __name__ == '__main__':
#    app.run(debug=True)
