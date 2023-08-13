from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL, Email

class RentalForm(Form):
    vehicle_id = IntegerField(
        'Vehicle ID', validators=[DataRequired()]
    )
    customer_id = IntegerField(
        'Customer ID', validators=[DataRequired()]
    )
    rentaldate = DateTimeField(
        'Rental Date',
        validators=[DataRequired()],
        default=datetime.today()
    )
    returndate = DateTimeField(
        'Return Date',
        validators=[DataRequired()],
        default=datetime.today()
    )
    totalcost = IntegerField(
        'Total Cost', validators=[DataRequired()]
    )

class VehicleForm(Form):
    brand = StringField(
        'Brand', validators=[DataRequired()]
    )
    model = StringField(
        'Model', validators=[DataRequired()]
    )
    year = StringField(
        'Year', validators=[DataRequired()]
    )
    color = StringField(
        'Color', validators=[DataRequired()]
    )
    phone = StringField(
        'Phone', validators=[DataRequired()]
    )
    rentalprice = StringField(
        'Rental Price', validators=[DataRequired()]
    )


class CustomerForm(Form):
      firstname = StringField(
        'First Name', validators=[DataRequired()]
       )
      lastname = StringField(
        'Last Name', validators=[DataRequired()]
       )
      email = StringField(
        'Email', validators=[DataRequired(), Email()]
       )
      phone = StringField(
        'Phone', validators=[DataRequired()]
       )
      address = StringField(
        'Address', validators=[DataRequired()]
       )