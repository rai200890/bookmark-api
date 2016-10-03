def assign_attributes(instance, params):
    for attribute, value in params.items():
        setattr(instance, attribute, value)
