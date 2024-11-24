import uuid

def create_uuid():
    return str(uuid.uuid4()).replace("-", "")    

def generate_id(id_length:int, min_id_length:int, max_id_length:int):
    unique_id = create_uuid()
    if id_length < min_id_length:
        raise Exception("id length cannot be lower then min id length")
    if id_length > max_id_length:
        raise Exception("id length cannot be longer then max id length")
    
    while len(unique_id) < id_length:
        unique_id += create_uuid()
        
    result = unique_id[:id_length]
    if not result:
        raise Exception("no id was generated")
    return result
