def assign_attributes(instance, params):
    for attribute, value in params.items():
        setattr(instance, attribute, value)


def handle_delete(model, id):
    deleted_records = model.query.filter_by(id=id).delete()
    if deleted_records > 0:
        return None, 204
    return None, 422
