# updateIfNotNull(FieldName: str, change):
# contains the string to update 'Field' to a new entry if the given `change`` is non-empty
def updateIfNotNull(FieldName: str, change):
    if change != None:
        return (FieldName + " = " + str(change))
    else:
        return ""

# uINN(FieldName: str, change):
# alias for updateIfNotNull
def uINN(FieldName: str, change):
    return updateIfNotNull(FieldName, change)