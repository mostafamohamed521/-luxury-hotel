from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .models import Payment
from .forms import PaymentForm

@login_required
def checkout(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, user=request.user)
    if hasattr(booking, 'payment') and booking.payment.status == 'completed':
        return redirect('booking_detail', pk=booking.pk)
    form = PaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        card_num = data['card_number'].replace(' ', '')
        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                'amount': booking.total_price,
                'method': data['method'],
                'card_last_four': card_num[-4:],
                'card_brand': 'Visa' if card_num.startswith('4') else 'Mastercard',
                'status': 'completed',
                'transaction_id': f"TXN{booking.booking_ref}",
            }
        )
        if not created:
            payment.status = 'completed'
            payment.save()
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, "Payment successful! Your booking is confirmed.")
        return redirect('payment_success', booking_pk=booking.pk)
    return render(request, 'payments/checkout.html', {'booking': booking, 'form': form})

@login_required
def payment_success(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, user=request.user)
    return render(request, 'payments/success.html', {'booking': booking})
