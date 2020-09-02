
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, session, url_for
import random
import functools
import sys

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = "super secret key"

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://jh3958:6273@35.231.103.173/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS survivor (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO survivor(name) VALUES ('jonny fairplay'), ('boston rob'), ('sandra');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None
    
@app.before_request
def load_logged_in_user():
    user_id = session.get('User_ID')

    if user_id is None:
        g.user = None
    else:
        g.user = g.conn.execute(
            'SELECT * FROM Listener WHERE User_ID = (%s)', (user_id)
        ).fetchone()

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass



#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT network_name FROM network")
  networkNames = []
  for result in cursor:
#     networkNames.append(result['name'])  # can also be accessed using result[0]
    networkNames.append(result[0])  # can also be accessed using result[0]
  cursor.close()

  cursor = g.conn.execute("SELECT show_name FROM show")
  showNames = []
  for result in cursor:
    showNames.append(result[0])  # can also be accessed using result[0]
    
    
  cursor = g.conn.execute("SELECT title FROM episode")
  episodeTitles = []
  for result in cursor:
    episodeTitles.append(result[0])  # can also be accessed using result[0]
    
  cursor = g.conn.execute("SELECT name FROM host")
  hostNames = []
  for result in cursor:
    hostNames.append(result[0])  # can also be accessed using result[0]
    
  cursor = g.conn.execute("SELECT name FROM guest")
  guestNames = []
  for result in cursor:
    guestNames.append(result[0])  # can also be accessed using result[0]
  
  cursor = g.conn.execute("SELECT User_name FROM Listener")
  ListenerNames = []
  for result in cursor:
    ListenerNames.append(result[0])  # can also be accessed using result[0]
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(host = hostNames, guest = guestNames, network = networkNames, show = showNames, episode = episodeTitles)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

@app.route('/menuTemplate')
def menuPage():

    return render_template("menuTemplate.html")

@app.route('/testIndex')
def testPage():

    return render_template("testIndex.html")


#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/networks')
def networkPage():
    cursor = g.conn.execute("SELECT network_name FROM network")
    networkNames = []
    for result in cursor:
#     networkNames.append(result['name'])  # can also be accessed using result[0]
        networkNames.append(result[0])  # can also be accessed using result[0]
    cursor.close()
    context = dict(networks = networkNames)

    return render_template("networks.html", **context)

##### Making individual pages.

@app.route('/episodes')
def episodePage():
    cursor = g.conn.execute("SELECT title FROM episode")
    episodeNames = []
    for result in cursor:
#     networkNames.append(result['name'])  # can also be accessed using result[0]
        episodeNames.append(result[0])  # can also be accessed using result[0]
    cursor.close()
    context = dict(episodes = episodeNames)

    return render_template("episodes.html", **context)

@app.route('/hosts')
def hostPage():
    cursor = g.conn.execute("SELECT name FROM host")
    hostNames = []
    for result in cursor:
        hostNames.append(result[0])  # can also be accessed using result[0]
    cursor.close()
    context = dict(hosts = hostNames)

    return render_template("hosts.html", **context)


@app.route('/shows')
def showPage():
    cursor = g.conn.execute("SELECT show_name FROM show")
    showNames = []
    for result in cursor:
        showNames.append(result[0])  # can also be accessed using result[0]
    cursor.close()
    context = dict(shows = showNames)

    return render_template("shows.html", **context)


@app.route('/listener')
def listenerPage():
    cursor = g.conn.execute("SELECT User_name FROM Listener")
    userNames = []
    for result in cursor:
        userNames.append(result[0])  # can also be accessed using result[0]
    cursor.close()
    context = dict(listeners = userNames)

    return render_template("listeners.html", **context)




# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        
        error = None

        if not username:
            error = 'Username is required.'
        elif g.conn.execute(
            'SELECT User_ID FROM Listener WHERE User_name = (%s)', username
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            id = g.conn.execute("SELECT count(User_ID) FROM Listener")
            id_count = []
            for result in id:
                id_count.append(result[0])
            id_count = id_count[0]+1
            g.conn.execute(
                'INSERT INTO Listener (User_ID,User_name) VALUES (%s, %s)', (id_count, username)
            )
            
            return redirect('/')

    return render_template('register.html')


#@app.route('/login')
#def login():
#    abort(401)
#    this_is_never_executed()

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        error = None
        user = g.conn.execute(
            'SELECT User_ID FROM Listener WHERE User_name = (%s)', (username,)
        )
        user_id = []
        for result in user:
            user_id.append(result[0])

        if user is None:
            error = 'Incorrect username.'

        if error is None:
            session.clear()
            session['User_ID'] = float(user_id[0])
            return redirect(url_for('index'))


    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

#test for saving dynamic favourites list
@app.route('/savefave', methods=['POST'])
def savefave():
    id = session.get("User_ID")
    favList = request.form.getlist('favs[]')
    
    def get_fav_person(fav):
        p_id_cursor = g.conn.execute(
            "SELECT Person_ID FROM Person WHERE Name = (%s)", (fav)
        )
        p_ids = []
        for result in p_id_cursor:
            p_ids.append(result[0])
        p_id = float(p_ids[0])
        return p_id
    
    def check_fav(fav):
        if g.conn.execute(
                'SELECT Person_ID FROM Person WHERE Name = (%s)', fav
            ).fetchone() is not None:
            p_id = get_fav_person(fav)
        else:
            p_id = None
        if g.conn.execute(
            'SELECT Person_ID FROM saved_podcasters WHERE Person_id = (%s) AND User_ID = %s', (p_id), (id)
        ).fetchone() is not None:
            error = '%s already favorited', p_id
            return error
        elif g.conn.execute(
            'SELECT * FROM saved_episodes WHERE Title = (%s) AND User_ID = %s', (fav), (id)
        ).fetchone() is not None:
            error = '%s already favorited', fav
            return error
        elif g.conn.execute(
            'SELECT * FROM saved_network WHERE Network_name = (%s) AND User_ID = %s', (fav), (id)
        ).fetchone() is not None:
            error = '%s already favorited', fav
            return error
        elif g.conn.execute(
            'SELECT * FROM saved_shows WHERE show_name = (%s) AND User_ID = %s', (fav), (id)
        ).fetchone() is not None:
            error = '%s already favorited', fav
            return error
        return
       
            
        
                          
    for fav in favList:
        error = check_fav(fav)
        if error is None:
            if g.conn.execute(
                'SELECT Person_ID FROM Person WHERE Name = (%s)', fav
            ).fetchone() is not None:
                p_id = get_fav_person(fav)
                g.conn.execute(
                    "INSERT INTO saved_podcasters (User_ID, Person_ID) Values (%s, %s)", (id), (p_id)
                )
            elif g.conn.execute(
                'SELECT Show_name FROM episode WHERE Title = (%s)', fav
            ).fetchone() is not None:
                g.conn.execute(
                "INSERT INTO saved_episodes (User_ID, Title) Values (%s, %s)", (id), (fav)
                )
            elif g.conn.execute(
                'SELECT * FROM network WHERE Network_name = (%s)', fav
            ).fetchone() is not None:
                g.conn.execute(
                "INSERT INTO saved_network (User_ID, Network_name) Values (%s, %s)", (id), (fav)
                )
            elif g.conn.execute(
                'SELECT * FROM show WHERE show_name = (%s)', fav
            ).fetchone() is not None:
                g.conn.execute(
                "INSERT INTO saved_shows (User_ID, show_name) Values (%s, %s)", (id), (fav)
                )
        else:
            return error
    return redirect('/')

@app.route('/deletefave', methods=['POST'])
def deletefave():
    id = session.get("User_ID")
    favList = request.form.getlist('favs[]')
    
    def get_fav_person(fav):
        p_id_cursor = g.conn.execute(
            "SELECT Person_ID FROM Person WHERE Name = (%s)", (fav)
        )
        p_ids = []
        for result in p_id_cursor:
            p_ids.append(result[0])
        p_id = float(p_ids[0])
        return p_id 
                          
    for fav in favList:
        if g.conn.execute(
                'SELECT Person_ID FROM Person WHERE Name = (%s)', fav
            ).fetchone() is not None:
            p_id = get_fav_person(fav)
        else:
            p_id = None
        if g.conn.execute(
            'SELECT Person_ID FROM saved_podcasters WHERE Person_ID = (%s) AND User_ID = %s', (p_id), (id)
        ).fetchone() is not None:
            g.conn.execute(
                "DELETE FROM saved_podcasters WHERE Person_id = %s AND User_ID = %s", (p_id), (id)
            )
        elif g.conn.execute(
            'SELECT * FROM saved_episodes WHERE Title = (%s) AND User_ID = %s', (fav), (id)
        ).fetchone() is not None:
            g.conn.execute(
            "DELETE FROM saved_episodes WHERE Title = %s AND User_ID = %s", (fav), (id)
            )
        elif g.conn.execute(
            'SELECT * FROM saved_network WHERE Network_name = (%s) AND User_ID = %s', (fav), (id)
        ).fetchone() is not None:
            g.conn.execute(
            "DELETE FROM saved_network WHERE Network_name = (%s) AND User_ID = %s", (fav), (id)
            )
        elif g.conn.execute(
            'SELECT * FROM saved_shows WHERE show_name = (%s) AND User_ID = %s', (fav), (id)
        ).fetchone() is not None:
            g.conn.execute(
            "DELETE FROM saved_shows WHERE show_name = (%s) AND User_ID = %s", (fav), (id)
            )
    return redirect('/')


@app.route('/saved')
@login_required
def saved():
    id = session.get("User_ID")
    episode_cursor = g.conn.execute(
        'SELECT title FROM saved_episodes WHERE User_Id = (%s)',(id)
    )
    episodeNames = []
    for result in episode_cursor:
        episodeNames.append(result[0])
        
    person_cursor = g.conn.execute(
        'SELECT Name FROM Person WHERE Person_ID IN (SELECT Person_ID FROM saved_podcasters WHERE User_Id = (%s))',(id)
    )
    personNames = []
    for result in person_cursor:
        personNames.append(result[0])
        
    network_cursor = g.conn.execute(
        'SELECT Network_name FROM saved_network WHERE User_Id = (%s)',(id)
    )
    networkNames = []
    for result in network_cursor:
        networkNames.append(result[0])
        
    show_cursor = g.conn.execute(
        'SELECT show_name FROM saved_shows WHERE User_Id = (%s)',(id)
    )
    showNames = []
    for result in show_cursor:
        showNames.append(result[0])
    
    context = dict(shows = showNames, networks = networkNames, people = personNames, episodes = episodeNames)
    if id is None:
        abort(404, "User id {0} doesn't exist.".format(id))


    return render_template('saved.html', **context)

@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete():
    db.execute('DELETE Network_name FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@app.route('/hostdetails/<hostname>')
def hostdetails(hostname):
     
    show_cursor = g.conn.execute(
        "SELECT a.Show_name FROM(SELECT * FROM hosts_show, host WHERE host.Person_ID = hosts_show.Person_ID) as a WHERE a.name = %s", (hostname)
    )
    showNames = []
    for result in show_cursor:
        showNames.append(result[0])  # can also be accessed using result[0]
    show_cursor.close()
    
    if g.conn.execute(
            'SELECT Person_ID FROM guest WHERE name = (%s)', hostname
        ).fetchone() is not None:
        guest_cursor = g.conn.execute(
        "SELECT a.Title FROM (SELECT * FROM appears_on_episode, guest WHERE guest.Person_ID = appears_on_episode.Person_ID) as a WHERE a.name = %s", (hostname)
        )
        appears_on = []
        for result in guest_cursor:
            appears_on.append(result[0])
        guest_cursor.close()
        context = dict(shows = showNames, guest_shows = appears_on)
    else:    
        context = dict(shows = showNames)
    
    return render_template('hostdetails.html', hostname = hostname, **context)

@app.route('/networkdetails/<networkname>')
def networkdetails(networkname):
    show_cursor = g.conn.execute(
        "SELECT show_name FROM show WHERE Network_name = %s", (networkname)
    )
    showNames = []
    for result in show_cursor:
        showNames.append(result[0])  # can also be accessed using result[0]
    show_cursor.close()
    context = dict(shows = showNames)
    return render_template('networkdetails.html', networkname = networkname, **context)

@app.route('/showdetails/<showname>')
def showdetails(showname):
    epi_cursor = g.conn.execute(
        "SELECT Title FROM episode WHERE Show_name = %s", (showname)
    )
    epiNames = []
    for result in epi_cursor:
        epiNames.append(result[0])  # can also be accessed using result[0]
    epi_cursor.close()
    
    host_cursor = g.conn.execute(
        "SELECT host.name FROM (SELECT a.Person_ID FROM(SELECT show.Show_name, hosts_show.Person_ID FROM hosts_show, show WHERE show.Show_name = hosts_show.Show_name) as a WHERE a.Show_name = %s) as b, host WHERE host.Person_ID = b.Person_ID", (showname)
    )
    hostNames = []
    for result in host_cursor:
        hostNames.append(result[0])  # can also be accessed using result[0]
    host_cursor.close()
    if g.conn.execute(
            'SELECT Network_name FROM show WHERE show_name = (%s)', (showname)
        ).fetchone() is not None:
        network_cursor = g.conn.execute("SELECT Network_name From show WHERE Show_name = %s", (showname))
        networkNames = []
        for result in network_cursor:
            networkNames.append(result[0])
        context = dict(episodes = epiNames, hosts=hostNames, network=networkNames)
    else:
       context = dict(episodes = epiNames, hosts=hostNames)
        
    return render_template('showdetails.html', showname = showname, **context)

@app.route('/episodedetails/<epiname>')
def episodedetails(epiname):
    epi_cursor = g.conn.execute(
        "SELECT * FROM episode WHERE Title = %s", (epiname)
    )
    epiNames = []
    for result in epi_cursor:
        epiNames.append(result[0:])  # can also be accessed using result[0]
    epi_cursor.close()
    context = dict(episodes = epiNames)
    return render_template('episodedetails.html', epiname = epiname, **context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
