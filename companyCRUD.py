from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/companies'
db = SQLAlchemy(app)
mallow = Marshmallow(app)


class Company(db.Model):
    comp_id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.Unicode)
    emp_count = db.Column(db.Integer)
    comp_loc = db.Column(db.Unicode)
    comp_email = db.Column(db.Unicode)
    comp_ind = db.Column(db.Unicode)

    def __init__(self, comp_name, emp_count, comp_loc, comp_email, comp_ind):
        self.comp_name = comp_name
        self.emp_count = emp_count
        self.comp_loc = comp_loc
        self.comp_email = comp_email
        self.comp_ind = comp_ind


class CompanySchema(mallow.Schema):
    class Meta:
        fields = ('comp_id', 'comp_name', 'emp_count', 'comp_loc', 'comp_email', 'comp_ind')


comp_schema = CompanySchema()
comps_schema = CompanySchema(many=True)


# route for adding new company
@app.route("/company", methods=["POST"])
def add_comp_rec():
    comp_name = request.json['comp_name']
    emp_count = request.json['emp_count']
    comp_loc = request.json['comp_loc']
    comp_email = request.json['comp_email']
    comp_ind = request.json['comp_ind']

    new_comp = Company(comp_name, emp_count, comp_loc, comp_email, comp_ind)
    db.session.add(new_comp)
    db.session.commit()

    return jsonify(comp_schema.dump(new_comp))


# route for retrieving all company records
@app.route("/company", methods=["GET"])
def get_comp_recs():
    all_comps = Company.query.all()
    return jsonify(comps_schema.dump(all_comps))


# route for retrieving a company record by id
@app.route("/company/<int:comp_id>", methods=["GET"])
def get_comp_rec_id(comp_id):
    comp = Company.query.get(comp_id)
    return jsonify(comp_schema.dump(comp))


# route for retrieving a company record by name
@app.route("/company/<comp_name>", methods=["GET"])
def get_comp_rec_name(comp_name):
    comp = ''
    if '*' in comp_name:
        if comp_name.count('*') == 2:
            comp = Company.query.filter(Company.comp_name.like("%"+comp_name.replace("*", "")+"%")).all()
        elif comp_name.find('*') == 0:
            comp = Company.query.filter(Company.comp_name.like("%"+comp_name.replace("*", ""))).all()
        else:
            comp = Company.query.filter(Company.comp_name.like(comp_name.replace("*", "")+"%")).all()
    else:
        comp = Company.query.filter_by(comp_name=comp_name).all()

    return jsonify(comps_schema.dump(comp))


# route for updating a company record by id
@app.route("/company/<int:comp_id>", methods=["PUT"])
def update_comp_rec_id(comp_id):
    comp = Company.query.get(comp_id)
    comp_name = request.json['comp_name']
    emp_count = request.json['emp_count']
    comp_loc = request.json['comp_loc']
    comp_email = request.json['comp_email']
    comp_ind = request.json['comp_ind']

    comp.comp_name = comp_name
    comp.emp_count = emp_count
    comp.comp_loc = comp_loc
    comp.comp_email = comp_email
    comp.comp_ind = comp_ind

    db.session.commit()
    return jsonify(comp_schema.dump(comp))


# route for updating a company record by name
@app.route("/company/<comp_name>", methods=["PUT"])
def update_comp_rec_name(comp_name):
    comp = Company.query.filter_by(comp_name=comp_name).first()
    comp_name = request.json['comp_name']
    emp_count = request.json['emp_count']
    comp_loc = request.json['comp_loc']
    comp_email = request.json['comp_email']
    comp_ind = request.json['comp_ind']

    comp.comp_name = comp_name
    comp.emp_count = emp_count
    comp.comp_loc = comp_loc
    comp.comp_email = comp_email
    comp.comp_ind = comp_ind

    db.session.commit()
    return jsonify(comp_schema.dump(comp))


# route for deleting a company record by id
@app.route("/company/<int:comp_id>", methods=["DELETE"])
def delete_comp_rec_id(comp_id):
    comp = Company.query.get(comp_id)
    db.session.delete(comp)
    db.session.commit()

    return jsonify(comp_schema.dump(comp))


# route for deleting a company record by name
@app.route("/company/<comp_name>", methods=["DELETE"])
def delete_comp_rec_name(comp_name):
    comp = Company.query.filter_by(comp_name=comp_name).first()
    db.session.delete(comp)
    db.session.commit()

    return jsonify(comp_schema.dump(comp))


if __name__ == '__main__':
    app.run(debug=True)
