from rest_framework.validators import ValidationError

def non_negative_int(val):
    if val < 0:
        raise ValidationError("The field cant be negative")