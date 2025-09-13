# upgrade_api.py
import re
from pathlib import Path

APP = Path("app.py")
src = APP.read_text(encoding="utf-8")

def ensure_json_sort_keys_false(code: str) -> str:
    # After "app = Flask(__name__)" insert JSON_SORT_KEYS=False if missing
    if 'JSON_SORT_KEYS' in code:
        return code
    pattern = r'(app\s*=\s*Flask\(\s*__name__\s*\)\s*)'
    replacement = r"\1\n\n# Keep field order in JSON responses stable & human-friendly\napp.config['JSON_SORT_KEYS'] = False\n"
    return re.sub(pattern, replacement, code, count=1)

def insert_before_entrypoint(code: str, block: str) -> str:
    # Insert our block right before the "if __name__ == '__main__':" guard
    marker = r'\n#\s*-+\s*\n#\s*Entry\s*\n#\s*-+\s*\nif __name__ == "__main__":'
    if "### BEGIN APLUS EXTRAS ###" in code:
        return code  # already inserted
    return re.sub(marker, f"\n\n{block}\n\n\\g<0>", code, count=1)

EXTRA_BLOCK = r'''
### BEGIN APLUS EXTRAS ###
# -------------------------------
# A+++ rubric upgrades (idempotent)
# -------------------------------

# 1) Uniform JSON error responses for common HTTP errors
from flask import abort

@app.errorhandler(404)
def _json_404(e):
    # Only emit our JSON when a route doesn't exist; re-use existing not_found for resources
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(405)
def _json_405(e):
    return jsonify({"error": "Method Not Allowed"}), 405

@app.errorhandler(500)
def _json_500(e):
    # Do not leak stack traces in JSON; your debug server will still show them in console
    return jsonify({"error": "Internal Server Error"}), 500


# 2) Lightweight guard: require JSON for POST/PUT with bodies
@app.before_request
def _require_json_for_mutations():
    # Only enforce for endpoints that usually accept bodies
    if request.method in {"POST", "PUT"}:
        # Some tools set no Content-Type for empty bodies; accept those
        if request.data and request.mimetype != "application/json":
            return jsonify({"error": "Content-Type must be application/json"}), 400


# 3) Bonus rubric endpoints: order totals & user order summaries
def _order_total(o: "Order") -> float:
    # Sum prices for all products currently in the order
    return float(sum((p.price or 0.0) for p in getattr(o, "products", [])))

@app.get("/orders/<int:order_id>/total")
def get_order_total(order_id: int):
    order = Order.query.get(order_id)
    if not order:
        return not_found("Order not found")
    return jsonify({"order_id": order.id, "total": _order_total(order)})

@app.get("/orders/user/<int:user_id>/summary")
def get_user_orders_summary(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return not_found("User not found")
    orders = Order.query.filter_by(user_id=user_id).all()
    payload = []
    for o in orders:
        payload.append({
            "order_id": o.id,
            "order_date": o.order_date.isoformat() if o.order_date else None,
            "product_count": len(o.products),
            "total": _order_total(o),
        })
    return jsonify(payload)

### END APLUS EXTRAS ###
'''.strip()

# Apply patches
src = ensure_json_sort_keys_false(src)
src = insert_before_entrypoint(src, EXTRA_BLOCK)

# Save
APP.write_text(src, encoding="utf-8")
print("✅ app.py upgraded for A+++ rubric: JSON errors, JSON guard, totals & summaries, JSON_SORT_KEYS=False.")
