def recursive_errors_to_dict(errors, keys, value):
    key = keys[0]
    if len(keys) == 1:
        if key in errors:
            if isinstance(errors[key], list):
                errors[key].append(value)
            else:
                errors[key] = [errors[key], value]
        else:
            errors[key] = [value]
    else:
        next_key = keys[1]
        if isinstance(next_key, int):
            next_key = str(next_key)
        if key not in errors:
            errors[key] = {}
        recursive_errors_to_dict(errors[key], [next_key] + list(keys[2:]), value)
