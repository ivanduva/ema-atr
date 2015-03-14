from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class HistoricoForm(Form):
    tm_inicio = StringField('TimeStamp inicio')
    tm_fin = StringField('TimeStamp fin')
