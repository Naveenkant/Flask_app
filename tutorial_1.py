from flask import Flask, redirect, url_for,render_template,request,session,jsonify
from datetime import timedelta
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app =Flask(__name__)
app.secret_key="Naveen"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users:sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime=timedelta(minutes=5)

db=SQLAlchemy(app)

class Movies(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    movieName=db.Column(db.String(100))
    date = db.Column(db.DateTime)
    zoner=db.Column(db.String(100))
    

    def __init__(self,movieName,date,zoner):
        self.movieName=movieName
        self.date=date
        self.zoner=zoner

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html",values=Movies.query.all())

@app.route("/addMovie",methods=["POST","GET"])
def addMovie():
    if request.method=="POST":
        session.permanent=True
        movieName=request.form["movieName"]
        date_str=request.form["releasingDate"]
        zoner=request.form["zoner"]
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        print(date,"\n\n\n\n")
        found_movie = Movies.query.filter_by(movieName=movieName).first()

        if found_movie:
            print("Movie already exists.")
        else:
            data=Movies(movieName,date,zoner)
            db.session.add(data)
            db.session.commit()

        return redirect(url_for("view"))
        
    else:
        return render_template("movie.html")  

@app.route("/getMovie/<int:movie_id>", methods=["GET"])
def getMovie(movie_id):
    movie = Movies.query.get(movie_id)

    if movie:
       
        return jsonify(
            id=movie._id,
            movieName=movie.movieName,
            date=str(movie.date),  
            zoner=movie.zoner
        )
    else:
        return jsonify({"error": "Movie not found"}) 

@app.route("/updateMovie/<int:movie_id>",methods=["POST","GET"])
def updateMovie(movie_id):
    if request.method=="POST":
        new_movie_name=request.form["newMovieName"]
        movie_to_update=Movies.query.get(movie_id)

        if(movie_to_update):
            movie_to_update.movieName=new_movie_name
            db.session.commit()
            return redirect(url_for("view"))
        
        else:
            return jsonify("Movie not found")

    else:
        movie_to_update=Movies.query.get(movie_id)

        if(movie_to_update):
            return render_template("update_movie.html",movie=movie_to_update)
        
        else:
            return jsonify("Movie not found")


@app.route("/deleteMovie/<int:movie_id>",methods=["GET"])
def deleteMovie(movie_id):
    movie_to_delete=Movies.query.get(movie_id)

    if(movie_to_delete):
        db.session.delete(movie_to_delete)
        db.session.commit()

        return redirect(url_for("view"))
    else:
        return jsonify("Movie not found or Already Deleted")
    

@app.route("/deleteAllMovies", methods=["GET"])
def deleteAllMovies():
    Movies.query.delete()
    db.session.commit()

    return redirect(url_for("view"))


if __name__ == "__main__":
    
    app.run(debug=True)

with app.app_context():
    db.create_all()