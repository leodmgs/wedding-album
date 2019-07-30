from os import path
from uuid import uuid4
from datetime import datetime
from app.main.database import DB


class Photo(object):

    def __init__(self, data, accepted=False, counter_like=0):
        self.photo_data = data
        fname, fext = path.splitext(self.photo_data.filename)
        self.uuid_filename = str(uuid4().hex) + fext
        self.accepted = accepted
        self.counter_like = counter_like
        self.created_at = datetime.utcnow()

    def filename(self):
        return self.uuid_filename

    def insert(self):
        inserted_id = DB.insert(collection='photos', data=self.json())
        if inserted_id:
            # FIXME: Images must be stored on Amazon S3
            # self.photo_data.save(path.join('/tmp/uploads', self.uuid_filename))
            return True
        return False

    def json(self):
        return {
            'filename': self.uuid_filename,
            'accepted': self.accepted,
            'counter_like': self.counter_like,
            'created_at': self.created_at
        }
