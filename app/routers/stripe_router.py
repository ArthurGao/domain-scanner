# app/routers/stripe_router.py
import os

import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/stripe")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class CheckoutSessionRequest(BaseModel):
    priceId: str


@router.post("/create-checkout-session")
def create_checkout_session(data: CheckoutSessionRequest):
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": data.priceId, "quantity": 1}],
            success_url="http://localhost:5173/success",
            cancel_url="http://localhost:5173/",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
