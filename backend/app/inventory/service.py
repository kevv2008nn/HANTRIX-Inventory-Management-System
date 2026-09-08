from sqlalchemy.orm import Session

from app.models.inventory import Inventory


def create_inventory(
    db: Session,
    data
):

    item = Inventory(
        component_id=data.component_id,
        component_name=data.component_name,
        category=data.category,
        description=data.description,
        rack=data.rack,
        shelf=data.shelf,
        location_code=data.location_code,
        quantity=data.quantity,
        minimum_quantity=data.minimum_quantity,
        qr_code=data.qr_code,
        rfid_tag=data.rfid_tag,
        condition=data.condition,
        status=data.status,
        image_path=data.image_path,
        detection_label=data.detection_label,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_all_inventory(db: Session):

    return (
        db.query(Inventory)
        .order_by(Inventory.component_name.asc())
        .all()
    )


def get_inventory(
    db: Session,
    component_id: str
):

    return (
        db.query(Inventory)
        .filter(
            Inventory.component_id == component_id
        )
        .first()
    )


def update_inventory(
    db: Session,
    component_id: str,
    data
):

    item = get_inventory(
        db,
        component_id
    )

    if not item:
        return None

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            item,
            key,
            value
        )

    db.commit()
    db.refresh(item)

    return item


def delete_inventory(
    db: Session,
    component_id: str
):

    item = get_inventory(
        db,
        component_id
    )

    if not item:
        return None

    db.delete(item)
    db.commit()

    return True