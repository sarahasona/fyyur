#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,abort,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from config import *
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.sql import label
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#New Define Migrate -- sara--
migrate = Migrate(app,db)
# TO_DO: connect to a local postgresql database
# Doooooone
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    venue_show = db.relationship('Show',back_populates='venue',lazy=True)

# TO_DO: implement any missing fields, as a database migration using Flask-Migrate
#Dooone in Venues --sara--
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    artist_show = db.relationship('Show',back_populates='artist',lazy=True)

# TO_DO: implement any missing fields, as a database migration using Flask-Migrate
#Doooe missing fields Artis--sara--

# TO_DO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#Dooone Define association table show --sara--
class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable=False)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=False)
    start_date = db.Column(db.DateTime,nullable=False)
    venue = db.relationship('Venue',back_populates='venue_show')
    artist = db.relationship('Artist',back_populates='artist_show')
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TO_DO: replace with real venues data.
  #Dooone replace with real venues data. --sara--
  Error = False
  try:  
    VenuesData = []
    #Get Venue data grouping by state and city
    data3 = db.session.query(Venue.state.label('state'),Venue.city.label('city')).group_by(Venue.state,Venue.city).all() 
    for i in data3:
      Venuesarray = [] 
      #get Venus obect of city and state data   
      venuedataobjs = Venue.query.filter(Venue.state == i.state , Venue.city == i.city).all()    
      for obj in venuedataobjs: 
        currentdate = datetime.now()
        #get count of Upcoming Shows
        getUpcomingShows = Show.query.filter(Show.venue_id == obj.id , Show.start_date >= currentdate ).count()

        Venuesarray.append({'name' : obj.name , 'id' : obj.id ,'num_upcoming_shows' :getUpcomingShows})
      #append data obect to the VenuesData array
      VenuesData.append({"city": i.city ,"state": i.state ,"venues" : Venuesarray})
  
  except:
    Error = True
    print(sys.exc_info)
  if Error:
    abort(400)
  # num_shows should be aggregated based on number of upcoming shows per venue. 
  return render_template('pages/venues.html', areas=VenuesData)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TO_DO: implement search on artists with partial string search. Ensure it is case-insensitive.
  #Dooone --sara--
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  #get User search data
  searchdata = request.form.get('search_term')
  #get result according to the search data
  res = Venue.query.filter(Venue.name.ilike(f'%{searchdata}%')).all()
  #get Count of returning search result
  countRes = Venue.query.filter(Venue.name.ilike(f'%{searchdata}%')).count()
  responseArr =[]
  currentdate = datetime.now()
  for i in res:
    #get Upcomig show Count
    getUpcomingShows = Show.query.filter(Show.venue_id == i.id , Show.start_date >= currentdate ).count()
    responseArr.append({"id": i.id,"name": i.name,"num_upcoming_shows": getUpcomingShows})
  response = {"count" :countRes ,"data" :responseArr }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TO_DO: replace with real venue data from the venues table, using venue_id
  #Dooone --sara--
  currentDate = datetime.now()
  PastShowArr = []
  UpComingShowArr = []
  #get Venues Data 
  getVenue = Venue.query.get(venue_id)
  c = datetime.now()
  print('cccccccccc ',c)
  #join show with artist to get venue shows and venue data 
  showsdata = db.session.query(Show,Artist).join(Artist).filter(Show.venue_id == venue_id,Show.artist_id == Artist.id).all()
  print('showsdata  ',len(showsdata))
  for s in showsdata:
    p = s.Show.start_date
    print('ssssssssssssss  ' ,p)
    startdate = s.Show.start_date
    show_Artist = {"artist_id": s.Artist.id,
      "artist_name": s.Artist.name,
      "artist_image_link": s.Artist.image_link,
      "start_time": s.Show.start_date.strftime('%c')}
    if startdate < currentDate:
      PastShowArr.append(show_Artist)
    elif startdate > currentDate:
      UpComingShowArr.append(show_Artist) 

  data = {
    "id": getVenue.id,
    "name": getVenue.name,
    "address": getVenue.address,
    "city": getVenue.city,
    "state": getVenue.state,
    "phone": getVenue.phone,
    "facebook_link": getVenue.facebook_link,
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": getVenue.image_link,
    "past_shows": PastShowArr ,
    "upcoming_shows": UpComingShowArr,
    "past_shows_count": len(PastShowArr),
    "upcoming_shows_count": len(UpComingShowArr),
  } 
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  Error = False
  # TO_DO: insert form data as a new Venue record in the db, instead
  #Dooone --sara
  try:
    data = request.form
    #create new venue object and save to db 
    newVenue = Venue(
      name = data['name'],
      city = data['city'],
      state = data['state'],
      address = data['address'] ,
      phone = data['phone'],
      facebook_link = data['facebook_link'],
      image_link = data['image_link']  
      ) 
    db.session.add(newVenue)
    db.session.commit()
  except:
    Error = True
    print(sys.exc_info)
    db.session.rollback()
  finally:
    db.session.close()
  # TO_DO: on unsuccessful db insert, flash an error instead.
  #Dooone --sara--
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  if Error:
    abort(400)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # on successful db insert, flash success
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  # TO_DO: modify data to be the data object returned from db insertion

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<selectedid>/deleteVenue', methods=['DELETE'])
def delete_venue(selectedid):
  # TO_DO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  #Dooone --sara--
  Error = False
  try:
    #get venue of id = selectedid
    getVenue = Venue.query.get(selectedid)
    #get shows related to this venue
    getShow = Show.query.filter(Show.venue_id == selectedid).all()
    #if show list not empty delete show 
    if len(getShow) != 0:
      for i in getShow:
        db.session.delete(i)
    db.session.delete(getVenue)
    db.session.commit()
  except:
    Error = False
    print(sys.exc_info)
  if Error:
    abort(400) 

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  #Dooone --sara--
  # clicking that button delete it from the db then redirect the user to the homepage
  return jsonify({'success' : True})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TO_DO: replace with real data returned from querying the database
  #get artist data from db
  #Dooone replacing with real data --sara--
  #get artists data
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TO_DO: implement search on artists with partial string search. Ensure it is case-insensitive.
  #Dooone --sara--
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  #get user search data
  searchdata = request.form.get('search_term')
  #get list of artists filtered by search data
  res = Artist.query.filter(Artist.name.ilike(f'%{searchdata}%')).all()
  countRes = len(res)
  responseArr =[]
  currentdate = datetime.now()
  for i in res:
    getUpcomingShows = Show.query.filter(Show.artist_id == i.id , Show.start_date >= currentdate ).count()
    responseArr.append({"id": i.id,"name": i.name,"num_upcoming_shows": getUpcomingShows})
  response = {"count" :countRes ,"data" :responseArr }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TO_DO: replace with real venue data from the venues table, using venue_id
  #Dooone --sara--
  Error = False
  try:
    currentDate = datetime.now()
    PastShowArr = []
    UpComingShowArr = []
    #get Artist Data 
    getArtist = Artist.query.get(artist_id)
    #join show with venue to get artists shows and venue data 
    showsdata = db.session.query(Show,Venue).join(Venue).filter(Show.artist_id == artist_id,Show.venue_id == Venue.id).all()
    #dataaa = Show.query.join(Artist).filter(Show.artist_id == Artist.id).all()
    for s in showsdata:
      startdate = s.Show.start_date
      show_Venue = {"venue_id": s.Venue.id,
        "venue_name": s.Venue.name,
        "venue_image_link": s.Venue.image_link,
        "start_time": s.Show.start_date.strftime('%c')}
      if startdate< currentDate:
        PastShowArr.append(show_Venue)
      elif startdate > currentDate:
        UpComingShowArr.append(show_Venue)
    
    data = {
      "id": getArtist.id,
      "name": getArtist.name,
      "genres" : (getArtist.genres.replace('{', '').replace('}', '')).split(','),
      "city": getArtist.city,
      "state": getArtist.state,
      "phone": getArtist.phone,
      "facebook_link": getArtist.facebook_link,
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": getArtist.image_link,
      "past_shows": PastShowArr ,
      "upcoming_shows": UpComingShowArr,
      "past_shows_count": len(PastShowArr),
      "upcoming_shows_count": len(UpComingShowArr)
    }
  except:
    Error = True
    print(sys.exc_info)
  if Error:
    abort(400)       
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:id>/edit', methods=['GET'])
def edit_artist(id):
  form = ArtistForm()
  getArtist = Artist.query.get(id)
  data = {
    "id": getArtist.id,
    "name": getArtist.name,
    "genres": getArtist.genres,
    "city": getArtist.city,
    "state": getArtist.state,
    "phone": getArtist.phone,
    "facebook_link": getArtist.facebook_link,
    "image_link": getArtist.image_link
    }
  form.name.data = getArtist.name
  form.city.data = getArtist.city
  form.state.data = getArtist.state
  form.phone.data = getArtist.phone
  form.facebook_link.data = getArtist.facebook_link
  form.image_link.data = getArtist.image_link
  form.genres.data = getArtist.genres 
  # TO_DO: populate form with fields from artist with ID <artist_id>
  #Dooone
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  Error = False
  try:
    data = request.form
    GenresArray = data.getlist('genres')
    get_artist = Artist.query.get(artist_id)
    get_artist.name = data['name']
    get_artist.city = data['city']
    get_artist.state = data['state']
    get_artist.phone = data['phone']
    get_artist.facebook_link = data['facebook_link']
    get_artist.image_link = data['image_link']
    get_artist.genres = GenresArray
    db.session.commit()
  except:
    Error = True
    print(sys.exc_info)
    db.session.rollback()
  finally:
    db.session.close()
  if Error:
    abort(400)
    flash('An error occurred.')
  # on successful db insert, flash success
  else:
    flash('Artist Updated Successfuly')

  # TO_DO: take values from the form submitted, and update existing
  #Dooone --sara--
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  getVenue = Venue.query.get(venue_id)
  venuedata={
    "id": getVenue.id,
    "name": getVenue.name,
    "address": getVenue.address,
    "city": getVenue.city,
    "state": getVenue.state,
    "phone": getVenue.phone,
    "facebook_link": getVenue.facebook_link,
    "image_link": getVenue.image_link
    }
  form.name.data = getVenue.name
  form.address.data = getVenue.address
  form.city.data = getVenue.city
  form.state.data = getVenue.state
  form.phone.data = getVenue.phone
  form.facebook_link.data = getVenue.facebook_link
  form.image_link.data = getVenue.image_link
  # TO_DO: populate form with values from venue with ID <venue_id>
  #Dooone --sara--
  return render_template('forms/edit_venue.html', form=form, venue=venuedata)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TO_DO: take values from the form submitted, and update existing
  #Dooone --sara--
  Error = False
  try:
    print(venue_id)
    data = request.form
    get_Venue = Venue.query.get(venue_id)
    get_Venue.name = data['name']
    get_Venue.city = data['city']
    get_Venue.state = data['state']
    get_Venue.phone = data['phone']
    get_Venue.address = data['address']
    get_Venue.facebook_link = data['facebook_link']
    get_Venue.image_link = data['image_link']
    print(get_Venue)
    db.session.commit()
  except:
    Error = True
    print(sys.exc_info)
    db.session.rollback()
  finally:
    db.session.close()
  if Error:
    abort(400)
    flash('An error occurred.')
  # on successful db insert, flash success
  else:
    flash('Venue Updated Successfuly')
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  #form = CreateUserForm(request.form)
  # called upon submitting the new artist listing form
  # TO_DO: insert form data as a new artist record in the db, instead
  #Dooone--sara--
  
  GenresArray = []
  Error = False
  try:
    data = request.form
    GenresArray = data.getlist('genres')
    print("data     " , data )    
    newArtist = Artist(
      name = data['name'],
      city = data['city'],
      state = data['state'],
      phone = data['phone'],
      facebook_link = data['facebook_link'],
      image_link = data['image_link'],
      genres = GenresArray
      )
    print("newArtist     " , newArtist ) 
    db.session.add(newArtist)
    db.session.commit()
  except:
    Error = True
    print(sys.exc_info)
    db.session.rollback()
  finally:
    db.session.close()
  if Error:
    abort(400)
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  # on successful db insert, flash success
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  # TO_DO: modify data to be the data object returned from db insertion

  # TO_DO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TO_DO: replace with real venues data.
  #Dooone --sara--
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  Shows = Show.query.all()
  for i in Shows:
    Artists = Artist.query.get(i.artist_id)
    Venues = Venue.query.get(i.venue_id)
    if Artist and Venues:
      data.append({
        "venue_id": i.venue_id,
        "venue_name": Venues.name,
        "artist_id": i.artist_id,
        "artist_name": Artists.name,
        "artist_image_link": Artists.image_link,
        "start_time": i.start_date
      })

  data1=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TO_DO: insert form data as a new Show record in the db, instead
  #Dooone --sara--
  Error = False
  try:
    data = request.form
    artistid=data['artist_id']
    Venueid = data['venue_id']
    getArtist = Artist.query.get(artistid)
    getVenue = Venue.query.get(Venueid)
    if getArtist and getVenue:
      newShow = Show(
      venue_id = data['venue_id'],
      artist_id = data['artist_id'],
      start_date = data['start_time']
      ) 
      db.session.add(newShow)
      db.session.commit()
    else:
      flash('An error occurred Venue or Artist not found')
      Error = True
   
  except:
    Error = True
    print(sys.exc_info)
    db.session.rollback()
  finally:
    db.session.close()
  if Error:
    abort(400)
    flash('An error occurred')
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')  
  # TO_DO: on unsuccessful db insert, flash an error instead.
  #Dooone --sara--
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
