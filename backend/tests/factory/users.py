from faker import Faker
import uuid
fake = Faker()

def create_fake_user(user_id=str(uuid.uuid4()),with_id:bool=True,with_password:bool=True) -> dict:
    fake_user = {
        "username":fake.user_name(),
        "email":fake.email(),
        "first_name":fake.name(),
        "last_name":fake.name()
    }
    if with_id:
        fake_user['id']= user_id

    if with_password:
        fake_user['password']= fake.password()
        
    return fake_user
