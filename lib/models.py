import mongoengine as me

class Group(me.Document):
  access_code = me.StringField(required=True)
  description = me.StringField(required=True)
  rules = me.StringField()
  created = me.DateTimeField()
  meta = {
    'auto_create_index': True,
    'index_opts': { 'expireAfterSeconds': 259200 },
    'indexes': [
      {
          'fields': ['created'],
          'expireAfterSeconds': 259200
      }
    ]
  }

class Connection(me.Document):
  sid = me.StringField(require=True, unique=True)
  group = me.StringField(require=True)
