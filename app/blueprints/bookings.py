"""Booking dashboard: create, list and cancel ticket bookings.

Every view is protected by ``login_required`` and scoped to the current
user, so one customer can never read or mutate another's bookings.
"""

from __future__ import annotations

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import BookingForm
from ..models import SEAT_PRICES, Booking

bookings_bp = Blueprint("bookings", __name__, url_prefix="/dashboard")


@bookings_bp.route("/")
@login_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    pagination = (
        Booking.query.filter_by(user_id=current_user.id)
        .order_by(Booking.created_at.desc())
        .paginate(page=page, per_page=8, error_out=False)
    )
    bookings = pagination.items
    total_spent = sum(b.total_price for b in current_user.bookings)
    total_seats = sum(b.seats for b in current_user.bookings)
    stats = {
        "total_bookings": len(current_user.bookings),
        "total_seats": total_seats,
        "total_spent": total_spent,
    }
    return render_template(
        "bookings/dashboard.html",
        bookings=bookings,
        pagination=pagination,
        stats=stats,
    )


@bookings_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            user_id=current_user.id,
            movie_name=form.movie_name.data.strip(),
            seat_class=form.seat_class.data,
            seats=form.seats.data,
            show_time=form.show_time.data,
            snacks=(form.snacks.data or "").strip() or None,
        )
        booking.total_price = booking.compute_total()
        db.session.add(booking)
        db.session.commit()
        flash("Your tickets are booked. Enjoy the show!", "success")
        return redirect(url_for("bookings.dashboard"))

    return render_template("bookings/create.html", form=form, seat_prices=SEAT_PRICES)


@bookings_bp.route("/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel(booking_id: int):
    booking = db.session.get(Booking, booking_id)
    if booking is None:
        abort(404)
    if booking.user_id != current_user.id:
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking cancelled.", "info")
    return redirect(url_for("bookings.dashboard"))
