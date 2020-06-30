from data_secure_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user):
    return User.query.get(str(user))


class User(db.Model, UserMixin):
    # eth_address: Ethereum blockchain address
    # id: hospital id given to patient
    # name: Name of Patient
    # dob: DOB of patient
    # address: actual address of patient
    # patient_id: hospital id
    # password: Password of user
    # degree: Degree posed by doctor
    # practice_id: govt practice id

    __tablename__ = 'user_details'
    eth_address = db.Column(db.String(42), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    dob = db.Column(db.String(20))
    address = db.Column(db.String(100))
    patient_id = db.Column(db.Integer, unique=True)

    degree = db.Column(db.String(30))
    practice_id = db.Column(db.Integer, unique=True)

    def get_id(self):
        return self.eth_address

    def __repr__(self):
        return f"User('{self.eth_address}','{self.password}', '{self.name}', '{self.role}')"


##################################################################################################################

class Patient(db.Model):
    # eth_address: Ethereum blockchain address
    # id: hospital id given to patient
    # name: Name of Patient
    # dob: DOB of patient
    # address: actual address of patient
    # password: Password of user

    __tablename__ = 'patient_details'
    eth_address = db.Column(db.String(42), primary_key=True)
    id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"Patient('{self.eth_address}','{self.password}', '{self.name}', '{self.id}', '{self.dob}'," \
            f" '{self.address}')"


class Doctor(db.Model):
    # eth_address: Ethereum blockchain address
    # practice_id: govt practice id
    # name: Name of Doctor
    # degree: Degree posed by doctor
    # password: Password of user

    __tablename__ = 'doctor_details'
    eth_address = db.Column(db.String(42), primary_key=True)
    id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"Doctor('{self.eth_address}','{self.password}', '{self.name}', '{self.practice_id}', '{self.degree}')"


class Admin(db.Model):
    # admin_name: Unique username for admin
    # password: password created to access admin page

    __tablename__ = 'admin_details'
    eth_address = db.Column(db.String(42), primary_key=True)
    admin_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"Admin('{self.admin_name}','{self.password}')"
