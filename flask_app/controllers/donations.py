from flask import render_template
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.donation import Donation  # Import your Donation model
from flask_app.models.user import User  # Import your Donation model
from flask_app.models.event import Event  # Import your Donation model
import paypalrestsdk


@app.route('/donations')
def donations():
    donations = Donation.get_all()  # Fetch all donations from the database
    return render_template('donations.html', donations=donations)



@app.route('/make_payment/<int:id>', methods=['POST'])
def checkoutPaypal(id):
    if 'user_id' not in session:
            return redirect('/logout')
    cmimi = request.form['amount']
    
    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AU7kx5FL4fR-TEb3NxegU6n9WeGskidUUEWBTXFu1-4sDxV4pFL-QBo9V49bzwU5IaQ44b7y8lKGySfz",
            "client_secret": "EE33b59GQKkk4nd_wXdQi8AHiSQOpfO98n4S-artHFSAArsDQIPWb429Cg5dXLhtcseh2fFzrJ9tm4g7"
        })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": cmimi,
                    "currency": "USD"  # Adjust based on your currency
                },
                "description": f"Nje donacion i ri!"
            }],
            "redirect_urls": {
                "return_url": url_for('paymentSuccess', _external=True, cmimi=cmimi, eventId = id),
                "cancel_url": "http://example.com/cancel"
            }
        })

        if payment.create():
            approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
            return redirect(approval_url)
        else:
            flash('Something went wrong with your payment', 'creditCardDetails')
            return redirect(request.referrer)
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'creditCardDetails')
        return redirect(request.referrer)






@app.route("/success", methods=["GET"])
def paymentSuccess():
    payment_id = request.args.get('paymentId', '')
    payer_id = request.args.get('PayerID', '')
    event_id = request.args.get('eventId', '')
    try:
        paypalrestsdk.configure({
            "mode": "sandbox", # Change this to "live" when you're ready to go live
            "client_id": "AU7kx5FL4fR-TEb3NxegU6n9WeGskidUUEWBTXFu1-4sDxV4pFL-QBo9V49bzwU5IaQ44b7y8lKGySfz",
            "client_secret": "EE33b59GQKkk4nd_wXdQi8AHiSQOpfO98n4S-artHFSAArsDQIPWb429Cg5dXLhtcseh2fFzrJ9tm4g7"
        })
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            
            
            ammount = request.args.get('cmimi')
            data = {
                'amount': ammount,
                'status': 'Successful',
                'user_id': session['user_id'],
                'event_id': event_id,
                'payment_method': 'Paypal'
            }
            User.create_payment(data)
            
            flash('Your payment was successful!', 'paymentSuccessful')
            return redirect('/success/payment')
            
        else:
            flash('Something went wrong with your payment', 'paymentNotSuccessful')
            return redirect('/')
    except paypalrestsdk.ResourceNotFound as e:
        flash('Something went wrong with your payment', 'paymentNotSuccessful')
        return redirect('/dashboard')


@app.route("/cancel", methods=["GET"])
def paymentCancel():
    flash('Payment was canceled', 'paymentCanceled')
    return redirect('/dashboard')


@app.route('/donate')
def donate():
    donation_type = request.args.get('type')
    event_id = request.args.get('event_id')
    
    if donation_type == 'money':
        # Fetch event data from the database based on event_id
        event = Event.get_event_by_id({'id': event_id})
        if not event:
            flash('Event does not exist.')
            return redirect('/donations')
        # Render donate.html with event data
        return render_template('donate.html', event=event)
    elif donation_type == 'clothes':
        # Render donate_clothes.html for clothes donations
        return render_template('donate_clothes.html')
    elif donation_type == 'books':
        # Render donate_books.html for books donations
        return render_template('donate_books.html')
    else:
        flash('Invalid donation type.')
        return redirect('/donations')
    
    
    
@app.route('/success/payment')
def success_payment():
    return render_template('sukses.html')