CUSTOMERS = {
    "user_123": {
        "name": "Mann",
        "email": "mann@example.com",
        "plan": "premium",
        "tenant_id" : "tenant_abc"
    },
    "user_456": {
        "name": "Rahul",
        "email": "rahul@example.com",
        "plan": "basic",
        "tenant_id" : "tenant_xyz"
    },
}

def get_customer(customer_id: str, tenant_id : str) -> dict:
    customer = CUSTOMERS.get(customer_id)

    if not customer:
        raise ValueError("Customer not found")

    if customer["tenant_id"] != tenant_id:
        raise PermissionError("Customer does not belong to this tenant")

    return customer