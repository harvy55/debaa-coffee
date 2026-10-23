from pyscript import window, document
from pyodide.ffi import create_proxy

def handle_order_calculation(event):
    """Event handler for calculating order totals dynamically."""
    if event:
        event.preventDefault()

    # Retrieve values from DOM elements
    base_price = float(document.getElementById("drink-select").value)
    size_upgrade = float(document.getElementById("cup-size").value)
    quantity_raw = document.getElementById("quantity").value
    extra_shot = document.getElementById("add-shot").checked
    promo = document.getElementById("discount-code").value.strip().upper()

    output_div = document.getElementById("receipt-output")

    # Input Validation
    try:
        quantity = int(quantity_raw)
        if quantity <= 0:
            show_message(output_div, "Please enter a valid quantity greater than zero.", is_error=True)
            return
    except ValueError:
        show_message(output_div, "Please enter a valid number for quantity.", is_error=True)
        return

    # Itemized price calculations
    unit_price = base_price + size_upgrade + (30.0 if extra_shot else 0.0)
    subtotal = unit_price * quantity

    # Calculate discount code
    discount = 0.0
    if promo == "DEBAA10":
        discount = subtotal * 0.10  # 10% discount

    total = subtotal - discount

    # Event-Driven Dynamic Webpage Update
    summary_html = f"""
        <h3>Order Confirmation</h3>
        <p><strong>Item Unit Cost:</strong> ₱{unit_price:.2f}</p>
        <p><strong>Quantity:</strong> {quantity}</p>
        <p><strong>Subtotal:</strong> ₱{subtotal:.2f}</p>
        <p><strong>Discount applied:</strong> -₱{discount:.2f}</p>
        <hr>
        <h4 style="color: #4a2c2a; font-size: 1.2rem;">Final Total: ₱{total:.2f}</h4>
    """
    
    show_message(output_div, summary_html, is_error=False)

def handle_feedback_submission(event):
    """Event handler for customer feedback form submission."""
    if event:
        event.preventDefault()

    name = document.getElementById("customer-name").value.strip()
    message = document.getElementById("customer-msg").value.strip()
    feedback_div = document.getElementById("feedback-alert")

    if not name or not message:
        show_message(feedback_div, "Please fill out both your name and feedback message.", is_error=True)
        return

    # Clear form fields on successful submission
    document.getElementById("customer-name").value = ""
    document.getElementById("customer-msg").value = ""

    success_text = f"Thank you, <strong>{name}</strong>! Your feedback has been received."
    show_message(feedback_div, success_text, is_error=False)

def show_message(element, content, is_error=False):
    """Utility helper to render messages to screen."""
    element.innerHTML = content
    element.style.display = "block"
    if is_error:
        element.style.backgroundColor = "#ffebee"
        element.style.borderLeft = "4px solid #c62828"
        element.style.color = "#c62828"
    else:
        element.style.backgroundColor = "#f1f8e9"
        element.style.borderLeft = "4px solid #33691e"
        element.style.color = "#1b5e20"

def setup_event_listeners():
    """Bind Python functions to HTML DOM events."""
    calc_button = document.getElementById("calc-btn")
    calc_button.addEventListener("click", create_proxy(handle_order_calculation))

    feedback_button = document.getElementById("submit-feedback-btn")
    feedback_button.addEventListener("click", create_proxy(handle_feedback_submission))

# Execute listener binding when script loads
setup_event_listeners()