import os
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from flask import Flask, request, jsonify
from flask.ext.restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from contextlib import closing


app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.py')
app.config.from_envvar('COMPLYNS_SETTINGS', silent=True)
db = SQLAlchemy(app)


def init_db():
  db.create_all()


class CRUD():

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class Packages(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(255))
    package_arch = db.Column(db.String(255))
    version_installed = db.Column(db.String(255))
    version_available = db.Column(db.String(255))
    fqdn = db.Column(db.String(255))

    def __init__(
            self,
            package_name,
            package_arch,
            version_installed,
            version_available,
            fqdn):
        self.package_name = package_name
        self.package_arch = package_arch
        self.version_installed = version_installed
        self.version_available = version_available
        self.fqdn = fqdn

    def __repr__(self):
        return '<Package %r>' % self.package_name


class PackagesSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannnot be blank')
    id = fields.Integer(dump_only=True)
    package_name = fields.String(validate=not_blank)
    package_arch = fields.String(validate=not_blank)
    version_installed = fields.String(validate=not_blank)
    version_available = fields.String(validate=not_blank)
    fqdn = fields.String(validate=not_blank)

    class Meta:
        type_ = 'packages'


schema = PackagesSchema()


class PackagesAPI(Resource):
    def get(self):
        app.logger.debug('request for package list')
        package_query = Packages.query.all()

        results = schema.dump(package_query, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            package = Packages(
                raw_dict['package_name'],
                raw_dict['package_arch'],
                raw_dict['version_installed'],
                raw_dict['version_available'],
                raw_dict['fqdn'])
            package.add(package)
            query = Packages.query.get(package.id)
            results = schema.dump(query).data
            return results, 201
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class PackagesUpdateAPI(Resource):
    def get(self, package_name):
        app.logger.debug('request for package info on %s', package_name)
        package_query = Packages.query.filter_by(package_name=package_name)
        results = schema.dump(package_query, many=True).data
        return results

    def put(self, package_name):
        app.logger.debug(
            'request for to add package %s with data %s',
            package_id,
            request.form['data']
        )
        packages[package_id] = request.form['data']
        return {package_id: packages[package_id]}


@app.route("/")
def index():
    return "hello"


api.add_resource(PackagesAPI, '/api/v1.0/packages/')
api.add_resource(PackagesUpdateAPI, '/api/v1.0/packages/<string:package_name>')

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
