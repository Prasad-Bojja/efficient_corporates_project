from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PaymentTransaction
import uuid
from .phonepe_api import PhonePe
from django.conf import settings  # Import settings for secure management of constants
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

MERCHANT_ID = settings.MERCHANT_ID
PHONE_PE_SALT = settings.PHONE_PE_SALT
PHONE_PE_HOST = settings.PHONE_PE_HOST
DJANGO_CUSTOM_REDIRECT_URL = settings.DJANGO_CUSTOM_REDIRECT_URL
DJANGO_CUSTOM_CALLBACK_URL = settings.DJANGO_CUSTOM_CALLBACK_URL
import logging

# Initialize the logger
logger = logging.getLogger('wallet')


#from django.views.decorators.csrf import ensure_csrf_cookie

@csrf_exempt
def create_payment_transaction(request):
    context = {}
    logger.info("create_payment_transaction view accessed")

    if request.method == 'POST':
        logger.debug("Processing POST request")
        amount = request.POST.get('amount')
        first_name = request.POST.get('first_name')
        email_id = request.POST.get('email_id')
        mobile = request.POST.get('mobile')

        # Validate amount
        if not amount:
            logger.warning("Amount is missing in the request")
            context['error'] = "Amount is required"
            return render(request, 'wallet/checkout.html', context)

        try:
            amount_float = float(amount)
            if amount_float <= 0:
                logger.warning("Invalid amount: Amount must be greater than zero")
                context['error'] = "Amount must be greater than zero"
                return render(request, 'wallet/checkout.html', context)
            amount_cents = int(amount_float * 100)
        except ValueError:
            logger.error("Invalid amount provided", exc_info=True)
            context['error'] = "Invalid amount format"
            return render(request, 'wallet/checkout.html', context)

        logger.debug("Amount validated successfully")
        
        # Initialize PhonePe integration
        phonepe = PhonePe(
            settings.MERCHANT_ID,
            settings.PHONE_PE_SALT,
            settings.PHONE_PE_HOST,
            settings.DJANGO_CUSTOM_REDIRECT_URL,
            settings.DJANGO_CUSTOM_CALLBACK_URL
        )
        
        # Create a unique order ID
        order_id = uuid.uuid4().hex
        try:
            order_data = phonepe.create_txn(order_id, amount_cents, email_id)
            logger.info("PhonePe transaction initiated")
        except Exception as e:
            logger.error("Error while creating transaction with PhonePe API", exc_info=True)
            context['error'] = "Error with payment API. Please try again."
            return render(request, 'wallet/checkout.html', context)

        redirect_url = order_data.get("data", {}).get("instrumentResponse", {}).get("redirectInfo", {}).get("url", "")
        if not redirect_url:
            logger.error("Missing redirect URL in response")
            context['error'] = "Payment initiation failed. Please contact support."
            return render(request, 'wallet/checkout.html', context)

        # Create payment transaction record
        transaction, created = PaymentTransaction.objects.get_or_create(
            first_name=first_name,
            email_id=email_id,
            mobile=mobile,
            order_id=order_id,
            defaults={
                'amount': amount_cents,
                'status': "PENDING",
                'message': order_data.get("message", ""),
                'payment_link': redirect_url,
                'base_amount': amount_float,
            }
        )

        if created:
            logger.info("Transaction created successfully")
            return redirect(redirect_url)
        else:
            logger.warning("Transaction already exists")
            context['error'] = "A transaction with this data already exists."
            return render(request, 'wallet/checkout.html', context)

    return render(request, 'wallet/checkout.html', context)


def home(request):
    return render(request, 'wallet/index.html')

@csrf_exempt
def payment_status(request):
    logger.info("payment_status view accessed")

    if request.method != 'POST':
        logger.warning("Invalid request method for payment_status")
        return HttpResponseBadRequest("Invalid request method. Only POST requests are allowed.")

    transaction_id = request.POST.get('transactionId')
    payment_status_code = request.POST.get('code')

    if not transaction_id or not payment_status_code:
        logger.warning("Missing transactionId or payment status code")
        return HttpResponseBadRequest("Missing transactionId or payment status code.")

    try:
        transaction = PaymentTransaction.objects.order_by('-create_at').first()
        if not transaction:
            logger.error("Transaction not found")
            return HttpResponseBadRequest("Transaction not found.")
    except PaymentTransaction.DoesNotExist:
        logger.error("Transaction does not exist in the database", exc_info=True)
        return HttpResponseBadRequest("Transaction not found.")

    transaction.transactionId = transaction_id
    if payment_status_code == 'PAYMENT_SUCCESS':
        transaction.status = 'SUCCESS'
        logger.info(f"Transaction {transaction_id} marked as SUCCESS")
    else:
        transaction.status = 'FAILED'
        logger.info(f"Transaction {transaction_id} marked as FAILED")

    transaction.save()

    context = {
        'message': f"Your transaction {transaction_id} was {'successful' if transaction.status == 'SUCCESS' else 'unsuccessful'}.",
        'alert_type': 'success' if transaction.status == 'SUCCESS' else 'danger',
    }

    return render(request, 'wallet/payment_status.html', context)