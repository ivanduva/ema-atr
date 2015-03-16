from webapp import db


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
        datatype = DataType.objects(name=name)
        if datatype is not None:
            datatype = datatype.filter(data__timestamp__gte=tm_inicio).filter(data__timestamp__lte=tm_fin).get()
            return datatype
        return None


class Data(db.EmbeddedDocument):
    timestamp = db.DateTimeField(required=True)
    value = db.StringField(required=True)

