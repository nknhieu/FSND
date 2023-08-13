#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
import datetime
from models import app, db, Vehicle, Customer, Rental
from forms import VehicleForm
from sqlalchemy.orm import joinedload
from auth.auth import AuthError, requires_auth
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

current_role = None
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')



@app.route('/vehicle')
# @requires_auth('get:vehicle')
def vehicle():
    data_vehicles = Vehicle.query.all()
    data = []
    for vehicle in data_vehicles:
        vehicle_data = {
            "id": vehicle.id,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "color": vehicle.color,
            "phone": vehicle.phone,
            "rentalprice": vehicle.rentalprice
        }
        data.append(vehicle_data)
    return render_template('pages/vehicle.html', vehicles=data)
@app.route('/vehicle/search', methods=['POST'])
def search_vehicle():

    search_term = request.form['search_term']
    result_vehicles = Vehicle.query.filter(
        (Vehicle.brand.ilike(f'%{search_term}%')) |
        (Vehicle.model.ilike(f'%{search_term}%')) |
        (Vehicle.year.ilike(f'%{search_term}%')) |
        (Vehicle.color.ilike(f'%{search_term}%')) |
        (Vehicle.phone.ilike(f'%{search_term}%'))
    ).all()

    data_search = []
    for vehicle in result_vehicles:
        vehicle_data = {
            "id": vehicle.id,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "color": vehicle.color,
            "phone": vehicle.phone,
            "rentalprice": vehicle.rentalprice
        }
        data_search.append(vehicle_data)

    response = {
        "count": len(result_vehicles),
        "data": data_search
    }
    return render_template('pages/search_vehicle.html', results=response, search_term=search_term)

@app.route('/vehicles/<int:vehicle_id>')
# @requires_auth(permission='read')
def show_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    rental_history = []
    # rental_history = Rental.query.filter_by(vehicle_id=vehicle_id).all()
    rental_history = db.session.query(Rental).join(Customer).filter(Rental.vehicle_id == vehicle.id).all()
    print(rental_history)
    past_rentals = []
    upcoming_rentals = []

    for rental in rental_history:
        rental_info = {
            "customer_id": rental.customer_id,
            "customer_firstname": rental.customer.firstname,
            "customer_lastname": rental.customer.lastname,
            "customer_email": rental.customer.email,
            "rentaldate": str(rental.rentaldate),
            "returndate": str(rental.returndate),
            "totalcost": rental.totalcost
        }

        past_rentals.append(rental_info)

    data = {
        "id": vehicle.id,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "color": vehicle.color,
        "phone": vehicle.phone,
        "rentalprice": vehicle.rentalprice,
        "past_rentals": past_rentals,
        "upcoming_rentals": upcoming_rentals,
        "past_rentals_count": len(past_rentals),
        "upcoming_rentals_count": len(upcoming_rentals)
    }

    return render_template('pages/show_vehicle.html', vehicle=data)


#  
#  ----------------------------------------------------------------

@app.route('/vehicle/create', methods=['GET'])
def create_vehicle_form():
    form = VehicleForm()  
    return render_template('forms/new_vehicle.html', form=form)

@app.route('/vehicle/create', methods=['POST'])
def create_vehicle_submission():
    form = request.form
    
    new_vehicle = Vehicle(
        brand=form['brand'],
        model=form['model'],
        year=form['year'],
        color=form['color'],
        phone=form['phone'],
        rentalprice=int(form['rentalprice'])  # Chuyển đổi thành kiểu số nguyên
    )
    
    try:
        db.session.add(new_vehicle)
        db.session.commit()
        flash('Vehicle ' + form['brand'] + ' ' + form['model'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Vehicle ' + form['brand'] + ' ' + form['model'] + ' could not be listed.')
    finally:
        db.session.close()
    
    return redirect(url_for('index'))



@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    deleted_vehicle = Vehicle.query.get(vehicle_id)
    vehicle_brand = deleted_vehicle.brand
    
    try:
        db.session.delete(deleted_vehicle)
        db.session.commit()
        flash('Vehicle ' + vehicle_brand + ' was successfully deleted!')
    except:
        db.session.rollback()
        flash('Please try again. Vehicle ' + vehicle_brand + ' could not be deleted.')
    finally:
        db.session.close()
    
    return redirect(url_for('index'))


#  Customer
#  ----------------------------------------------------------------
@app.route('/customers')
def customers():
    # Query data from the Customer model
    customers = Customer.query.all()

    return render_template('pages/customers.html', customers=customers)



@app.route('/customers/search', methods=['POST'])
def search_customers():
    # Get the search term from the form
    search_term = request.form['search_term']
    
    # Perform a case-insensitive search for customers with matching first name, last name, or email
    result_customers = Customer.query.filter(
        db.or_(
            Customer.firstname.ilike(f'%{search_term}%'),
            Customer.lastname.ilike(f'%{search_term}%'),
            Customer.email.ilike(f'%{search_term}%')
        )
    ).all()
    
    data_search = []
    for customer in result_customers:
        data_search.append({
            "id": customer.id,
            "firstname": customer.firstname,
            "lastname": customer.lastname,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address
        })

    response = {
        "count": len(result_customers),
        "data": data_search
    }
    return render_template('pages/search_customers.html', results=response, search_term=search_term)


@app.route('/customers/<int:customer_id>')
def show_customer(customer_id):
    # shows the customer page with the given customer_id
    # TODO: replace with real customer data from the customer table, using customer_id
    customer = Customer.query.get(customer_id)
    
    data = {
        "id": customer.id,
        "firstname": customer.firstname,
        "lastname": customer.lastname,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }

    return render_template('pages/show_customers.html', customer=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/customers/<int:customer_id>/edit', methods=['GET'])
def edit_customer(customer_id):
    form = CustomerForm()
  
    customer = Customer.query.get(customer_id)

    customer_info = {
        "id": customer.id,
        "firstname": customer.firstname,
        "lastname": customer.lastname,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }

    return render_template('forms/edit_customers.html', form=form, customer=customer_info)


@app.route('/customers/<int:customer_id>/edit', methods=['POST'])
def edit_customer_submission(customer_id):
    customer = Customer.query.get(customer_id)
    customer.firstname = request.form['firstname']
    customer.lastname = request.form['lastname']
    customer.email = request.form['email']
    customer.phone = request.form['phone']
    customer.address = request.form['address']
    try:
        db.session.commit()
        flash("Customer {} is updated successfully".format(customer.firstname))
    except:
        db.session.rollback()
        flash("Customer {} isn't updated successfully".format(customer.firstname))
    finally:
        db.session.close()
    return redirect(url_for('show_customer', customer_id=customer_id))


@app.route('/vehicles/<int:vehicle_id>/edit', methods=['GET'])
def edit_vehicle(vehicle_id):
    form = VehicleForm()
    vehicle = Vehicle.query.get(vehicle_id)
    vehicle_info = {
        "id": vehicle.id,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "color": vehicle.color,
        "phone": vehicle.phone,
        "rentalprice": vehicle.rentalprice
    }
    # TODO: populate form with values from vehicle with ID <vehicle_id>
    return render_template('forms/edit_vehicle.html', form=form, vehicle=vehicle_info)



@app.route('/vehicles/<int:vehicle_id>/edit', methods=['POST'])
def edit_vehicle_submission(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    
    vehicle.brand = request.form['brand']
    vehicle.model = request.form['model']
    vehicle.year = request.form['year']
    vehicle.color = request.form['color']
    vehicle.phone = request.form['phone']
    vehicle.rentalprice = request.form['rentalprice']

    try:
        db.session.commit()
        flash('Vehicle with ID {} was successfully updated!'.format(vehicle.id))
    except:
        db.session.rollback()
        flash('An error occurred. Vehicle with ID {} could not be updated.'.format(vehicle.id))
    finally:
        db.session.close()
    
    return redirect(url_for('show_vehicle', vehicle_id=vehicle_id))



@app.route('/customers/create', methods=['GET'])
def create_customer_form():
    form = CustomerForm()
    return render_template('forms/new_customers.html', form=form)


@app.route('/customers/create', methods=['POST'])
def create_customer_submission():
  form = request.form
  new_customer = Customer(
    firstname = form['firstname'],
    lastname = form['lastname'],
    email = form['email'],
    phone = form['phone'],
    address = form['address']
  )
  try:
    db.session.add(new_customer)
    db.session.commit()
    # On successful db insert, flash success
    flash('Customer ' + new_customer.firstname + ' ' + new_customer.lastname + ' was successfully listed!')
  except:
    db.session.rollback()
    # On unsuccessful db insert, flash an error instead.
    flash('An error occurred. Customer ' + new_customer.firstname + ' ' + new_customer.lastname + ' could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('index'))




@app.route('/rentals')
def rentals():
    # Retrieve a list of all rentals
    rentals_list = Rental.query.all()
    
    # Prepare data for rendering
    data = []
    for rental in rentals_list:
        data.append({
            "rental_id": rental.id,
            "vehicle_id": rental.vehicle_id,
            "customer_id": rental.customer_id,
            "rentaldate": rental.rentaldate.strftime('%Y-%m-%d %H:%M:%S'),
            "returndate": rental.returndate.strftime('%Y-%m-%d %H:%M:%S'),
            "totalcost": rental.totalcost
        })
    
    return render_template('pages/rentals.html', rentals=data)


@app.route('/rentals/create', methods=['GET'])
def create_rental_form():
    form = RentalForm()  
    return render_template('forms/new_rental.html', form=form)


@app.route('/rentals/create', methods=['POST'])
def create_rental_submission():
    form = request.form
    new_rental = Rental(
        vehicle_id=form['vehicle_id'],
        customer_id=form['customer_id'],
        rentaldate=form['rentaldate'],
        returndate=form['returndate'],
        totalcost=form['totalcost']
    )
    try:
        db.session.add(new_rental)
        db.session.commit()
        flash('Rental was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Rental could not be listed.')
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
