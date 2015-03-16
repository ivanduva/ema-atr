from flask.ext.wtf import Form
from wtforms import HiddenField, validators, TextField


class HistoricoForm(Form):
    tm_inicio = TextField('TimeStamp inicio', [validators.Required()])
    tm_fin = TextField('TimeStamp fin', [validators.Required()])
