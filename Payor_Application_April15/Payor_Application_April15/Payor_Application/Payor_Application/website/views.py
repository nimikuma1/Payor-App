from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Priorauth
from . import db
import json, requests
from sqlalchemy import text

views =  Blueprint('views',__name__)

@views.route('/')

def home():
   return render_template("login.html")


@views.route('/receive_prior_auth_request', methods=['POST'])
def receive_prior_auth_request():
    if request.method == 'POST':
        prior_auth_request = request.json
        #views.logger.info("Received prior auth request: %s", prior_auth_request)
        
       
        # Process the received request
        # Perform necessary actions

        # Construct response
        prior_auth_id = prior_auth_request.get('id')
        icd_code = prior_auth_request['supportingInfo'][1]['code']['coding'][0]['code']
        procedure_code = prior_auth_request['supportingInfo'][2]['code']['coding'][0]['code']
        payer = prior_auth_request['insurance'][0]['reference'].split('/')[-1]  # Extract payer ID
        member_name = prior_auth_request.get('subject', {}).get('display', None)  # Extract memberName

        # Check if memberID already exists in the Priorauth table
        existing_prior_auth = Priorauth.query.filter_by(memberID=int(prior_auth_id)).first()
        if existing_prior_auth:
        # MemberID already exists, handle accordingly (e.g., update existing entry or return an error)
        # For now, let's just log a message
            print(f"Prior authorization for memberID {prior_auth_id} already exists.")
        else:
            # MemberID does not exist, add to Priorauth table
            new_priorauth = Priorauth(
                memberID=int(prior_auth_id),
                memberName=member_name,
                payor=payer,
                ICDCode=icd_code,
                procedureCode=procedure_code,
                priorAuthStatus='Submitted'
            )  # Providing the schema for the prior authorization

        #new_priorauth = Priorauth(memberID=int(prior_auth_id),memberName =member_name,payor = payer,ICDCode = icd_code,procedureCode= procedure_code,priorAuthStatus = 'Submitted')  #providing the schema for the note
        db.session.add(new_priorauth) #adding the note to the database
        db.session.commit()
        # Define the SQL query
        #return redirect(url_for('views.emr'))
       
        #return render_template("payor.html", user=current_user)
        prior_auth_response = {
            "resourceType": "AuthorizationResponse",
            "id": prior_auth_id,
            "text": {
                "status": icd_code+payer+procedure_code,
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">AuthorizationResponse for Prior Authorization</div>"
            },
            "status": "complete",
            "authorizationStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "submitted",
                        "display": "Submitted"
                    }
                ]
            }
        }

        
        
        
        #flash("I am here")
        #id_number = prior_auth_request.get('id')
        #subject_reference = prior_auth_request['subject']['reference']
        #if subject_reference.startswith("Patient/"):
           # memberID_str = subject_reference.split('/')[-1]
        #member_ID = int(prior_auth_id)
        #flash(member_ID)
        # Extracting ICD code
        icd_code = prior_auth_request['supportingInfo'][1]['code']['coding'][0]['code']
        #flash(icd_code)
        # Extracting procedure code
        procedure_code = prior_auth_request['supportingInfo'][2]['code']['coding'][0]['code']
        payer = prior_auth_request['insurance'][0]['reference'].split('/')[-1]  # Extract payer ID


        #new_priorauth = priorauth(memberID=str(id_number),memberName =' ',payor = ' ',ICDCode = ' ',procedureCode= ' ' ,priorAuthStatus = 'Approved')  #providing the schema for the note
        #db.session.add(new_priorauth) #adding the note to the database
       # db.session.commit()
        return jsonify(prior_auth_response), 200
        #return render_template("payor.html", user=current_user)
    else:
        flash("I am here")
        return "Method not allowed", 405
    #return jsonify(prior_auth_response), 200

@views.route('/approve_request', methods=['POST'])
def approve_request():
        if request.method == 'POST':
        
            #new_priorauth = Priorauth(memberID=int(prior_auth_id),memberName =' ',payor = ' ',ICDCode = icd_code,procedureCode= procedure_code,priorAuthStatus = 'Approved')  #providing the schema for the note
            #db.session.add(new_priorauth) #adding the note to the database
            #db.session.commit()
            # Define the SQL query
            #return redirect(url_for('views.emr'))
            prior_auth_id = '1'
            #priorauth_data = Priorauth.query.all()
            #priorauth_data = Priorauth.query.filter_by(memberID=prior_auth_id).all()
            #return render_template('payor.html', priorauth_data=priorauth_data)
            #return render_template("payor.html", user=current_user)
            prior_auth_approval_response = {
                "resourceType": "AuthorizationResponse",
                "id": prior_auth_id,
                "text": {
                    "status": "generated",
                    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">AuthorizationResponse for Prior Authorization</div>"
                },
                "status": "complete",
                "authorizationStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                            "code": "approved",
                            "display": "Approved"
                        }
                    ]
                }
            }
              
            response = requests.post('http://localhost:5000/receive_prior_auth_approval_request', json=prior_auth_approval_response)
            #response_json = response.json()
            #submitted_value = response_json['authorizationStatus']['coding'][0]['display']

          
            #return jsonify(prior_auth_response), 200
            return render_template("payor.html", user=current_user)
        else:
            flash("I am here")
            return "Method not allowed", 405
        #return jsonify(prior_auth_response), 200



""""
        prior_auth_response = {
            "resourceType": "AuthorizationResponse",
            "id": prior_auth_id,
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">AuthorizationResponse for Prior Authorization</div>"
            },
            "status": "complete",
            "authorizationStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "approved",
                        "display": "Approved"
                    }
                ]
            }
        }

                sql_query = text(
            INSERT INTO Priorauth (memberID, memberName, payor, ICDCode, procedureCode, priorAuthStatus)
            VALUES (:member_id, :member_name, :payor, :icd_code, :procedure_code, :prior_auth_status)
        )
        connection = db.engine.connect()

        values = {
            'member_id': 1,
            'member_name': 'New Member Name',
            'payor': 'New Payor',
            'icd_code': 'New ICD Code',
            'procedure_code': 'New Procedure Code',
            'prior_auth_status': 'New Prior Auth Status'
        }
        # Execute the SQL query
        connection.execute(sql_query,**values)
        connection.commit()
        connection.close()
"""
