from flask import Flask, abort, redirect, url_for
from flask.ext.restful import Resource, Api, abort

from vegadns.api import endpoint
from vegadns.api.models.record import Record as ModelRecord


@endpoint
class Record(Resource):
    route = '/records/<int:record_id>'

    def get(self, record_id):
        try:
            record = self.get_record(record_id)
            typerecord = record.to_recordtype()
            return {'status': 'ok', 'record': typerecord.to_dict()}
        except:
            abort(404, message="record does not exist")
        return {'status': 'ok', 'record': record.to_dict()}

    def get_record(self, record_id):
        # FIXME authorization
        return ModelRecord.get(ModelRecord.record_id == record_id)

    def to_record_type():
        if self.type is None:
            raise Exception('Record type is not set')

        return AbstractRecordType.from_model(self)
