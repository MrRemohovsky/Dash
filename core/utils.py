from models import db


def bulk_create(list_to_create):
    db.session.add_all(list_to_create)
    db.session.commit()