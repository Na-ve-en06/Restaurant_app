from datetime import timedelta
from .. import schemas
from fastapi import HTTPException,APIRouter
from app.DB import get_db_connection
from app.schemas import OrderRequest,datetime
from decimal import Decimal

router = APIRouter(    prefix="/order",
    tags=['order']
)

@router.post("/orders")
def place_order(order: OrderRequest):
    conn = get_db_connection()
    cur = conn.cursor()

    # 1️⃣ Get cart items
    cur.execute("""
        SELECT m.menu_id, m.price, c.quantity
        FROM cart_items c
        JOIN menu_table m ON c.menu_id = m.menu_id
        WHERE c.user_id = %s
    """, (order.user_id,))
    items = cur.fetchall()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty!")

    # 2️⃣ Calculate totals
    total = sum(row['price'] * row['quantity'] for row in items)
    cgst = Decimal(total) * Decimal("0.05")
    sgst = Decimal(total) * Decimal("0.05")
    grand_total = Decimal(total) + cgst + sgst

    # 3️⃣ Get default address
    cur.execute("""
        SELECT address FROM user_address
        WHERE user_id = %s AND is_default = TRUE LIMIT 1
    """, (order.user_id,))
    address_row = cur.fetchone()
    if not address_row:
        raise HTTPException(status_code=400, detail="No default address found!")

    # 4️⃣ Calculate order_time & delivery_time automatically
    order_time = datetime.now()
    delivery_time = order_time + timedelta(hours=1)

    # 5️⃣ Insert into orders table
    cur.execute("""
        INSERT INTO orders (
            user_id, order_items, address, status, order_time, delivery_time,
            total, cgst, sgst, grand_total, comments, discount_name, discount,
            payment_method, payment_made, transaction_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING order_id
    """, (
        order.user_id,
        ','.join(str(row["menu_id"]) for row in items),
        address_row['address'],
        order.status,
        order_time,
        delivery_time,
        Decimal(total), cgst, sgst, grand_total,
        order.comments, order.discount_name, Decimal(order.discount or 0.0),
        order.payment_method, order.payment_made, order.transaction_id
    ))

    new_order_id = cur.fetchone()['order_id']

    # 6️⃣ Clear cart
    cur.execute("DELETE FROM cart_items WHERE user_id = %s", (order.user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "✅ Order placed!",
        "order_id": new_order_id,
        "order_time": str(order_time),
        "delivery_time": str(delivery_time)
    }

@router.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Get order row
        cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cur.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found!")

        # Fix: convert to int list
        item_ids = [int(x.strip()) for x in order["order_items"].split(",")]

        # Now it matches integer = integer
        cur.execute(
            "SELECT menu_id, menu_name, price FROM menu_table WHERE menu_id = ANY(%s)",
            (item_ids,)
        )
        items_detail = cur.fetchall()
        order["items_detail"] = items_detail

        return {"order_details": order}

    finally:
        cur.close()
        conn.close()

