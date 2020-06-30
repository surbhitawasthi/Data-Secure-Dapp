from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, send_file
from data_secure_app import db, bcrypt
from data_secure_app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from data_secure_app.main.util import get_transaction_details
from data_secure_app.main.web3_functions import add_new_user, grant_permission_in_bc, revoke_permission_in_bc\
    , get_list_of_user_with_my_permission, get_list_of_user_files, add_file_hash_to_bc_by_doc, get_file_count\
    , get_balance, add_file_hash_to_bc
from data_secure_app.ipfs_manager.ipfs import add_file, get_file
from werkzeug.utils import secure_filename
import os
import json
import mimetypes

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        print(request.form)
        user = User.query.filter_by(eth_address=request.form['inputUsername']).first()
        if user and user.password == request.form['inputPassword']:
            global remember_flag
            remember_flag = False
            try:
                tmp = request.form['remember_me']
                print('tmp: ', tmp, type(tmp))
                if tmp and tmp == 'on':
                    remember_flag = True
                print(remember_flag)
            except Exception as e:
                print('exception in admin\n', e)
                remember_flag = False
            login_user(user, remember=remember_flag)

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Incorrect ID or Password', 'danger')

    return render_template('login.html', title="Data Secure Dapp", navbar_title="Data Secure Application")


@main.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    if current_user.eth_address == current_app.config['ADMIN_ADDR']:
        return redirect(url_for('main.admin'))

    print(current_user.eth_address)
    user_type = current_user.role
    tmp = get_list_of_user_files(current_user.eth_address, current_user.eth_address)
    filenames = []
    if tmp[1]:
        filenames = tmp[0]
    # [{'filename': 'f1.jpg', 'fileIPFSHash': 'VDJNKJ65'}]
    user_details = []
    tmp = get_list_of_user_with_my_permission(current_user.eth_address)
    if tmp[1]:
        user_details = tmp[0]
    # [{'name': 'Surbhit', 'address': '0x53DE8E1b00591454e0C0315A342C148A68911234'}]
    transactions = get_transaction_details(current_user.eth_address)

    return render_template('dashboard.html', title="Dashboard", username=current_user.name, user_type=user_type,
                           filenames=filenames, user_details=user_details, transactions=transactions)


@main.route("/upload_file", methods=['POST'])
@login_required
def upload_file():
    try:
        f = request.files['file']
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(file_path)

        tmp = add_file(file_path, current_user.eth_address)

        file_object, uploaded = tmp[0], tmp[1]
        # print(file_object, uploaded)
        if not uploaded:
            flash('File Uploaded Unsuccessful', 'danger')
            return redirect(url_for('main.dashboard'))
        else:
            filename = file_object['Name'].split('/')[-1]
            if add_file_hash_to_bc(current_user.eth_address, filename, file_object['Hash']):
                flash('File Uploaded Successfully', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('File Uploaded Unsuccessful', 'danger')
                return redirect(url_for('main.dashboard'))
    except Exception as e:
        print('upload_file:\n', e)
        flash('File Uploaded Unsuccessful', 'danger')
        return redirect(url_for('main.dashboard'))


@main.route("/upload_file_for_patient", methods=['POST'])
@login_required
def upload_file_for_patient():
    try:
        patient_address = request.form['patient_address']
        f = request.files['file']
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(file_path)

        tmp = add_file(file_path, patient_address, doctor_address=current_user.eth_address)

        file_object, uploaded = tmp[0], tmp[1]

        if not uploaded:
            flash('File Uploaded for Patient Unsuccessful', 'danger')
            return redirect(url_for('main.dashboard'))
        else:
            filename = file_object['Name'].split('/')[-1]
            if add_file_hash_to_bc_by_doc(current_user.eth_address, patient_address, filename, file_object['Hash']):
                flash('File Uploaded for Patient Successfully', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('File Uploaded for Patient Unsuccessful', 'danger')
                return redirect(url_for('main.dashboard'))
    except Exception as e:
        print('upload_file_patient:\n', e)
        flash('File Uploaded for Patient Unsuccessful', 'danger')
        return redirect(url_for('main.dashboard'))


@main.route("/download_file", methods=['POST'])
@login_required
def download_file():
    fileName = request.json['fileName']
    user_address = request.json['user_address']
    search_bar = request.json['search_bar']
    if search_bar:
        print('True', current_user.eth_address, " ", user_address)
        a = get_file(fileName, person_accessing_address=current_user.eth_address, user_address=user_address)
    else:
        a = get_file(fileName, person_accessing_address=current_user.eth_address, user_address=current_user.eth_address)
    print(a)
    if a == '403':
        return jsonify({'error': 'Unauthorised Access'}), 403
    elif a == '500':
        return jsonify({'error': 'Internal Server Error'}), 500
    elif a == '404':
        return jsonify({'error': 'File Not Found'}), 404
    try:
        fileName = fileName.replace('.enc', '')
        fileName = os.path.join('../', current_app.config['DOWNLOAD_FOLDER'], secure_filename(fileName))  # why didnt use a????
#         print("hi " + fileName)
        content_type = mimetypes.guess_type(fileName)[0]
#         print(content_type)
        return send_file(fileName, content_type)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500


@main.route("/grant_permission", methods=['POST'])
@login_required
def grant_permission():
    print(request.form)
    granted_to = request.form['user_address']
    granted_by = current_user.eth_address
    try:
        if grant_permission_in_bc(granted_by, granted_to):
            flash('Permission Granted', 'success')
        else:
            flash('Permission Granting Failed', 'danger')
    except Exception as e:
        print('grant_user\n', e)
        flash('Permission Granting Failed', 'danger')

    return redirect(url_for('main.dashboard'))


@main.route("/revoke", methods=['POST'])
@login_required
def revoke():
    print(request.form)
    revoked_for = request.form['revoke_user']
    revoked_by = current_user.eth_address
    try:
        if revoke_permission_in_bc(revoked_by, revoked_for):
            flash('Revoke Successful', 'success')
        else:
            flash('Revoke Failed', 'danger')
    except Exception as e:
        print('revoke_user\n', e)
        flash('Revoke Failed', 'danger')

    return redirect(url_for('main.dashboard'))


@main.route("/search", methods=['POST'])
@login_required
def search():
    user_address = request.json['searchString']
    print(user_address)
    tmp = get_list_of_user_files(access_karne_wala=current_user.eth_address, iski_files_hai=user_address)
    data, authorised = tmp[0], tmp[1]
    if not authorised:
        print('idhar')
        return jsonify({'error': 'Unauthorised Access'}), 401
    return json.dumps(data)


@main.route("/profile", methods=['GET'])
@login_required
def profile():
    if current_user.eth_address == current_app.config['ADMIN_ADDR']:
        return redirect(url_for('main.admin'))

    role = current_user.role
    user_data = {}
    if role == 'doc':
        user_data = {'eth_address': current_user.eth_address, 'name': current_user.name,
                     'practice_id': current_user.practice_id, 'degree': current_user.degree}
    elif role == 'pat':
        user_data = {'eth_address': current_user.eth_address, 'name': current_user.name,
                     'patient_id': current_user.patient_id, 'dob': current_user.dob, 'address': current_user.address}
    user_data['file_count'] = get_file_count(current_user.eth_address)
    user_data['balance'] = get_balance(current_user.eth_address)
    return render_template('profile.html', title="Profile", username=current_user.name, role=role, user_data=user_data)


@main.route("/logout", methods=['GET'])
@login_required
def logout():
    if current_user.eth_address == current_app.config['ADMIN_ADDR']:
        redirect(url_for('main.admin'))
    logout_user()
    return redirect(url_for("main.login"))


##################################################################################


@main.route("/admin", methods=['GET', 'POST'])
def admin():
    try:
        if current_user.eth_address == current_app.config['ADMIN_ADDR'] and current_user.is_authenticated:
            return redirect(url_for('main.add_patient'))
    except Exception as e:
        print(e)
    if request.method == 'POST':
        print(request.form)
        user = User.query.filter_by(eth_address=current_app.config['ADMIN_ADDR']).first()
        if user and user.name == request.form['inputUsername'] and user.password == request.form['inputPassword']:
            global remember_flag
            remember_flag = False
            try:
                tmp = request.form['remember_me']
                print('tmp: ', tmp, type(tmp))
                if tmp and tmp == 'on':
                    remember_flag = True
                print(remember_flag)
            except Exception as e:
                print('exception in login\n', e)
                remember_flag = False
            login_user(user, remember=remember_flag)
            return redirect(url_for('main.add_patient'))
        else:
            flash('Incorrect ID or Password', 'danger')

    return render_template('login.html', title='DSA: Admin Login', navbar_title="Data Secure Application: Admin Panel")


@main.route("/admin/add_patient", methods=['GET', 'POST'])
@login_required
def add_patient():
    if current_user.eth_address == current_app.config['ADMIN_ADDR']:
        if request.method == 'POST':
            print(request.form)
            # ImmutableMultiDict([('patient_name', 'pat1'), ('eth_address', '0x54654'), ('password', 'asd'),
            # ('patient_id', '145'), ('patient_dob', '01/01/1988'), ('patient_add', 'sadcdsac')])
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            # print(hashed_password)
            patient = User()
            patient.eth_address = request.form['eth_address']
            patient.name = request.form['patient_name']
            patient.password=request.form['password']
            patient.role = 'pat'

            patient.dob = request.form['patient_dob']
            patient.address = request.form['patient_add']
            patient.patient_id = int(request.form['patient_id'])

            try:
                if add_new_user(current_user.eth_address, patient.eth_address, patient.name, False):
                    db.session.add(patient)
                    db.session.commit()
                    flash('Patient account created', 'success')
                else:
                    flash('Patient not created', 'danger')
            except Exception as e:
                print(e)
                flash('Patient not created', 'danger')

        return render_template('add_user.html', user_type='patient', title='Add Patient', username=current_user.name)
    else:
        return redirect(url_for('main.login'))


@main.route("/admin/add_doctor", methods=['GET', 'POST'])
@login_required
def add_doctor():
    if current_user.eth_address == current_app.config['ADMIN_ADDR']:
        if request.method == 'POST':
            print(request.form)
            # ImmutableMultiDict([('doctor_name', 'doc1'), ('eth_address', '0x7777'), ('password', 'sad'),
            # ('practice_id', '2356'), ('degree', 'MBBS, MD')])
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            # print(hashed_password)
            doctor = User()
            doctor.eth_address = request.form['eth_address']
            doctor.name = request.form['doctor_name']
            doctor.password = request.form['password']
            doctor.role = 'doc'

            doctor.practice_id = int(request.form['practice_id'])
            doctor.degree = request.form['degree']

            try:
                if add_new_user(current_user.eth_address, doctor.eth_address, doctor.name, True):
                    db.session.add(doctor)
                    db.session.commit()
                    flash('Doctor account created', 'success')
                else:
                    flash('Doctor not created', 'danger')
            except Exception as e:
                print(e)
                flash('Doctor not created', 'danger')

        return render_template('add_user.html', user_type='doctor', title='Add Doctor', username=current_user.name)
    else:
        return redirect(url_for('main.login'))


@main.route("/admin_logout", methods=['GET'])
@login_required
def admin_logout():
    if current_user.eth_address == current_app.config['ADMIN_ADDR']:
        logout_user()
        return redirect(url_for("main.admin"))
    else:
        return redirect(url_for('main.login'))
