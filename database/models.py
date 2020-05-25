from .mongodb import db

class Group(db.Document):
  access_code = db.StringField(required=True, unique=True)
  description = db.StringField(required=True)
