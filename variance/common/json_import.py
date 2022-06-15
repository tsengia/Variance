from pathlib import Path

def import_models(ModelType: type, ModelSchema: type, import_path: object, session: object, exclude: tuple[str]=("id",)) -> int:
    """
    Helper function that loads all .json files from the provided import_path
    and turns them into ModelType instances and commits them to the database.
    
    Returns the number of ModelType instances committed.
    May raise an exception if there is an error while loading JSON data.
    """
    count = 0
    load_schema = ModelSchema(exclude=exclude)
    for j in import_path.glob("*.json"):
        d = load_schema.loads(j.read_text())
        m = ModelType(**d)
        session.add(m)
        count += 1    

    session.commit()
    return count
