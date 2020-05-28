import mongoengine as me

class Group(me.Document):
    access_code = me.StringField(required=True)
    description = me.StringField(required=True)
    rules = me.StringField()


# from .mongodb import db

# class Group(db.Document):
#   access_code = db.StringField(required=True, unique=True)
#   description = db.StringField(required=True)