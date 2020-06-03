import mongoengine as me

class Group(me.Document):
  name = me.StringField(required=True)
  access_code = me.StringField(required=True, unique=True)
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
  waiting = me.BooleanField(default=True)
  created = me.DateTimeField()
  user_name = me.StringField(default='Anonymous')
  last_match = me.StringField()
  meta = {
      'auto_create_index': True,
      'index_opts': {'expireAfterSeconds': 43200},
      'indexes': [
          {
              'fields': ['created'],
              'expireAfterSeconds': 43200
          }
      ]
  }
