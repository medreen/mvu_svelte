from flask import Flask, request, jsonify
from models import Base, User, Products, Sales, Payments
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.drop_all(engine)

# Create a session
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

# Initialize Bcrypt and JWT
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

# DEFINE YOUR ROUTES HERE
@app.route('/', methods=allowed_methods)
def home():
    method = request.method.lower()

    if method == "get":
        return jsonify({"Flask API Version" : "1.0"}),200
    else:
        return jsonify({"message":"Method not allowed"}),405

@app.route('/register', methods=allowed_methods)
def register():
    try:        
        if request.method != 'POST':
            return jsonify({'message': 'Method not allowed'}), 405

        data = request.get_json()
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')
        created_at = data.get('created_at', datetime.utcnow())

        if not full_name or not email or not password or not created_at:
            return jsonify({'message': 'Full name, email, and password are required'}), 400

        # Check if user already exists
        existing_user = db_session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User with this email already exists'}), 400

        # Hash the password
        hashed_password = generate_password_hash(password).decode('utf-8')

        # Create new user
        new_user = User(full_name=full_name, email=email, password=hashed_password, created_at=created_at)
        db_session.add(new_user)
        db_session.commit()

         # tokens generation
        access_token = create_access_token(identity=new_user.email)

        return jsonify({'message': 'User registered successfully', 'access_token': access_token}), 201


    except Exception as e:
        db_session.rollback()  # Rollback the session in case of an error
        return jsonify({'message': 'An error occurred during registration', 'error': str(e)}), 500

@app.route('/login', methods=allowed_methods)
def login():
    try:
        if request.method != 'POST':
            return jsonify({'message': 'Method not allowed'}), 405  

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        # Check if user exists
        email = email.lower().strip()  # Normalize email
        user = db_session.query(User).filter_by(email=email).first()
        print("User found:", user)  # Debugging statement
        if user and check_password_hash(user.password, password):        
            token = create_access_token(identity=user.email)

            return jsonify({
                "message": "Login successful!",
                "token": token
            }), 201  
        else:
            return jsonify({"error": "Invalid email or password"}), 401            
    except Exception as e:  
        db_session.rollback()       
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=allowed_methods)
@jwt_required()
def get_products():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user_email = get_jwt_identity()
            user = db_session.query(User).filter_by(email=user_email).first()

            if not user:
                return jsonify({'message': 'User not found'}), 404

            product_name = data.get('product_name')
            amount = data.get('amount')
            created_at = data.get('created_at', datetime.utcnow())

            if not product_name or not amount:
                return jsonify({'message': 'Product name and amount are required'}), 400

            new_product = Products(user_id=user.id, product_name=product_name, amount=float(amount), created_at=created_at)
            db_session.add(new_product)
            db_session.commit()

            return jsonify({'message': 'Product added successfully'}), 201
        
        elif request.method == 'GET':
            query = select(Products)
            products = db_session.scalars(query).all()

            product_list = []
            for i in products:
                product_list.append({
                "id" : i.id,
                "user_id": i.user_id,
                "product_name" : i.product_name,
                "amount" : i.amount,
                "created_at" : i.created_at 
                })
                
            return jsonify(product_list), 200

        else:
            return jsonify({"message":"Method not allowed"}), 405


    except Exception as e:
        db_session.rollback()
        return jsonify({'message': 'An error occurred while fetching products', 'error': str(e)}), 500

@app.route('/sales', methods=allowed_methods)
@jwt_required() 
def get_sales():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user_email = get_jwt_identity()
            user = db_session.query(User).filter_by(email=user_email).first()

            if not user:
                return jsonify({'message': 'User not found'}), 404

            product_id = data.get('product_id')
            created_at = data.get('created_at', datetime.utcnow())

            if not product_id:
                return jsonify({'message': 'Product ID is required'}), 400

            new_sale = Sales(product_id=product_id, created_at=created_at)
            db_session.add(new_sale)
            db_session.commit()

            return jsonify({'message': 'Sale recorded successfully'}), 201

       
        elif request.method == 'GET':
            query = select(Sales) 
            sales = db_session.scalars(query).all()

            sales_list = []
            for i in sales:
                sales_list.append({
                "id" : i.id,
                "product_id": i.product_id,
                "created_at" : i.created_at 
                })

            return jsonify(sales_list),200

        else:
            return jsonify({'message': 'Method not allowed'}), 405

    except Exception as e:
        db_session.rollback()
        return jsonify({'message': 'An error occurred while fetching sales', 'error': str(e)}), 500

@app.route('/stk-push', methods=allowed_methods)
@jwt_required()
def get_payments():
    try:
        data = request.get_json()

        # create a payment with only id,saleid,mrid,crid,created at
        sale_id = data.get('sale_id')
        trans_amount = data.get('amount')
        phone_paid = data.get('phone_number')

        if sale_id == None or trans_amount == None or  phone_paid == None:
            return jsonify({"error": "sale_id, phone_number and amount are required"}), 400
        
        stk_response = make_stk_push({
            "phone_number": phone_paid,
            "amount": trans_amount
        })
        print(stk_response)
        
        new_payment = Payment(
            sale_id=sale_id,
            mrid=stk_response.get("MerchantRequestID"),
            crid=stk_response.get("CheckoutRequestID"),
            phone_paid=phone_paid,
            trans_amount=float(trans_amount),
            status="Pending"
        )

        db_session.add(new_payment)
        db_session.commit()

        return jsonify({
            "message": "STK push sent",
            "response": stk_response,
            "phone_number": phone_paid,
            "amount": trans_amount
        }), 200
        
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/stk-call-back',methods = allowed_methods)
def call_back():
    data = request.get_json()
    print("stk callback data:-----------------",data)

    # fetch the payment record using mrid and crid
    query = select(Payment).where(Payment.mrid==data['Body']['stkCallback']['MerchantRequestID'],Payment.crid==data['Body']['stkCallback']['CheckoutRequestID'])  
    existing_payment = db_session.scalars(query).first()

    if int(data['Body']['stkCallback']['ResultCode'])==0:
        # update payment record with transaction code,transaction amount and status
        existing_payment.trans_code = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        existing_payment.status="Success"

    else:
        existing_payment.status="Failed"
        db_session.commit()

    return jsonify({"message":"callback received"}),200

@app.route('/mpesa-payments', methods=allowed_methods)
def mpesa_payments():
    try:
        method = request.method.lower()
        if method == 'get':
            query = select(Payment)
            payments = db_session.scalars(query).all()

            result = []

            for p in payments:
                result.append({
                    "id": p.id,
                    "sale_id": p.sale_id,
                    "mrid": p.mrid,
                    "crid": p.crid,
                    "trans_code": p.trans_code,
                    "trans_amount": p.trans_amount,
                    "phone_paid": p.phone_paid,
                    "status": p.status,
                    "created_at": p.created_at
                })

            return jsonify(result), 200
        else:
            return jsonify({"error":"Method not allowed"}),405

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(debug=True)