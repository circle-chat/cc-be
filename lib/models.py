import mongoengine as me

class Group(me.Document):
  access_code = me.StringField(required=True)
  description = me.StringField(required=True)
  rules = me.StringField()
