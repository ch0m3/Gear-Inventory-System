from flask import request
from app.gear.models.gear_model import (create_item, get_items, get_item, update_item_db, delete_item_db)
from app.utils.auth_required import login_required, role_required


def get_all_gear():
    items = get_items()
    return [dict(i) for i in items], 200


@login_required

@role_required("CM")
def create_gear():
    data = request.get_json()

    create_item(
        data["name"],
        data["price"],
        data["stock"]
    )

    return {"message": "Item created",
            "data": {
                "id": get_items()[-1]["id"],
                "name": data["name"],
                "price": data["price"],
                "stock": data["stock"]
            }
            }, 201


@login_required
@role_required("CM")
def update_gear(id):
    data = request.get_json()

    item = get_item(id)
    if not item:
        return {"error": "Not found"}, 404

    update_item_db(
        id,
        data.get("name", item["name"]),
        data.get("price", item["price"]),
        data.get("stock", item["stock"])
    )

    return {"message": "Updated"}, 200


@login_required
@role_required("CM")
def delete_gear(id):
    delete_item_db(id)
    return {"message": "Deleted"}, 200