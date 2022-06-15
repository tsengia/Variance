from pathlib import Path

def export_models(ModelType, ModelSchema, export_path, exclude=("id",)):
    """ 
    Helper function for querying all instances of ModelType,
    creating a folder at the export location, and creating a 
    JSON file for each model instance returned by the query.
    
    Returns a integer representing the number of models exported.
    """
    model_list = ModelTyle.query.all()
    dump_schema = ModelSchema(exclude=exclude)
    for m in model_list:
        cname = m.canonical_name
        f = location / (cname + ".json")
        f.write_text(dump_schema.dumps(m))

    return len(model_list)
