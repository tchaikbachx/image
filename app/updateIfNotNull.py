# updateIfNotNull(FieldName: str, change):
# contains the string to update 'Field' to a new entry if the given `change`` is non-empty.
# >> added another check condition
def updateIfNotNull(FieldName: str, change):
    if change is not None and change != "":
        # >> wrapped in single quotes if string
        if isinstance(change, str):
            return f"{FieldName} = '{change}'"
        return f"{FieldName} = {change}"
    else:
        return ""

# uINN(FieldName: str, change):
# alias for updateIfNotNull
def uINN(FieldName: str, change):
    return updateIfNotNull(FieldName, change)