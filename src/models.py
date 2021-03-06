from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Boolean, Column
from werkzeug.security import safe_str_cmp


db = SQLAlchemy()

class BaseModel():
    @classmethod
    def get_all(cls):
        return cls.query.all()
        

    @classmethod
    def get_one_by_id(cls,model_id):
        return cls.query.filter_by(id = model_id).first()


    @classmethod 
    def delete_all(cls):
        return cls.query.delete()
        

class User(db.Model,BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    last_name = Column(String(250))
    email= Column(String(250), nullable=False)
    password= Column(String(250), nullable=False)
    is_logged= Column(Boolean, default=False, nullable=False)
    token = Column(String(250), nullable=True)
    #Relation with favorites.
    Favorite_People = db.relationship('Favorite_People',backref='user', lazy=True)
    Favorite_Planets = db.relationship('Favorite_Planets', backref='user', lazy=True)

    def serializeFavorites(self):
        return {
            "id": self.id,
            "Favorite_People": list(map(lambda x: x.serializebyUser(), self.Favorite_People)),
            "Favorite_Planets": list(map(lambda x: x.serializebyUser(), self.Favorite_Planets)),
        }

    @staticmethod
    def login_credentials(email,password):
        return User.query.filter_by(email=email).filter_by(password=password).first()
    
    def user_have_token(self,token):
        return User.query.filter_by(token=self.token).first()
   
    def assign_token(self,token):
        self.token = token
        db.session.add(self)
        db.session.commit()
    
    def check_password(self, password_param):
        return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))
    
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "is_logged": self.is_logged,
            "Favorite_People": list(map(lambda x: x.serializebyUser(), self.Favorite_People)),
            "Favorite_Planets": list(map(lambda x: x.serializebyUser(), self.Favorite_Planets))
        }
    
    def serializeFavorites(self):
        return {
            "id": self.id,
            "Favorite_People": list(map(lambda x: x.serializebyUser(), self.Favorite_People)),
            "Favorite_Planets": list(map(lambda x: x.serializebyUser(), self.Favorite_Planets))
        }


class Planets(db.Model,BaseModel):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    population=Column(Integer,primary_key=False)
    orbital_period=Column(Integer,primary_key=False)
    rotation_period=Column(Integer,primary_key=False)
    diameter =Column(Integer,primary_key=False)
    Favorite_Planets = db.relationship('Favorite_Planets', backref='planets', lazy=True)
    

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "population": self.population,
            "orbital_period" :self.orbital_period,
            "rotation_period" : self.rotation_period,
            "diameter": self.diameter, 
            "Favorite_Planets": list(map(lambda x: x.serializebyPlanets(), self.Favorite_Planets)),
            # do not serialize the password, its a security breach
        }

        
    def db_post(self):        
        db.session.add(self)
        db.session.commit()

    def set_with_json(self,json):
        self.name = json["name"]
        self.population = json["population"]
        self.orbital_period = json["orbital_period"]
        self.rotation_period = json["rotation_period"]
        self.diameter = json["diameter"]

    def db_delete(self):
        db.session.delete(self)
        db.session.commit()

    

class People(BaseModel,db.Model):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    eye_color=Column(String(250))
    skin_color=Column(String(250))
    gender=Column(String(250))
    height = Column(String(250))
    description= Column(String(250))
    favorite_people = db.relationship('Favorite_People', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color":self.eye_color,
            "skin_color":self.skin_color,
            "gender":self.gender,
            "height":self.height,
            "description":self.description,
            "Favorite_People": list(map(lambda x: x.serializebyPeople(), self.Favorite_People))
            # do not serialize the password, its a security breach
        }
    
    def db_post(self):        
        db.session.add(self)
        db.session.commit()
    
    def set_with_json(self,json):
        self.name = json["name"]
        self.eye_color = json["eye_color"]
        self.skin_color = json["skin_color"]
        self.gender = json["gender"]
        self.height = json["height"]
        self.description = json["description"]
        
    def db_delete(self):
        db.session.delete(self)
        db.session.commit()


class Favorite_Planets(db.Model):
    __tablename__ = 'Favorite_Planets'
    tb_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))

    def __repr__(self):
        return '<Favorite_Planets %r>' % self.user_id
    
    def serializeByPlanet(self):
        return {
            "tb_id": self.tb_id,
            "planet_id": self.planet_id
        }
        
    def serializeByUser(self):
        return {
            "tb_id": self.id,
            "user_id": self.user_id,
        }

class Favorite_People(db.Model):
    __tablename__ = 'Favorite_People'
    tb_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))

    def __repr__(self):
        return '<Favorite_People %r>' % self.user_id
    
    def serializeByPeople(self):
        return {
            "tb_id": self.tb_id,
            "planet_id": self.person_id
        }
    def serializeByUser(self):
        return {
            "tb_id": self.id,
            "user_id": self.user_id,
        }

