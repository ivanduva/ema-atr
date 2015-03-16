from webapp import db
import time

class DataType(db.Document):
    name = db.StringField(max_length=255, required=True)
    type = db.StringField(required=True)
    data = db.ListField(db.EmbeddedDocumentField('Data'))

    def add_data(self, new_data):
        self.data.append(new_data)
        self.save()

    @staticmethod
    def get_or_create(name, type):
        datatype = DataType.objects(name=name).first()
        if datatype is None:
            datatype = DataType(name, type).save()
        return datatype

    @staticmethod
    def query_interval(name, tm_inicio, tm_fin):
        datatype = DataType.objects(name=name).exclude('id').filter(data__timestamp__gte=tm_inicio).filter(data__timestamp__lte=tm_fin).first()
        if datatype is not None:
            datatype.data = [d.to_dict() for d in datatype.data][::50]
            return datatype
        return None


class Data(db.EmbeddedDocument):
    timestamp = db.DateTimeField(required=True)
    value = db.StringField(required=True)

    def to_dict(self):
        return {"x": time.mktime(self.timestamp.timetuple()), "y": float(self.value)}
