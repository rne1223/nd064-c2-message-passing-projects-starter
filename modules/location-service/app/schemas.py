from models import Location
from geoalchemy2.types import Geometry as GeometryType
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter


class LocationSchema(Schema):
    id = fields.Integer()
    personId = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creationTime = fields.DateTime()

    class Meta:
        model = Location

