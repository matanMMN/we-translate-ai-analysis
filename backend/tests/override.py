from app.controllers import AuthController, TaskController, UserController
from app.models import Task, User
from meditranslate.src.auth.auth_service import AuthService
# from wetranslateai.src.users, import AuthService


class ServiceOverrides:
    def __init__(self, db_session):
        self.db_session = db_session

    def user_service(self):
        print("\n\n\n OVERRIDE \n\n\n")
        return UserController(UserRepository(model=User, session=self.db_session))

    def task_controller(self):
        return TaskController(TaskRepository(model=Task, session=self.db_session))

    def auth_service(self):
        return AuthController(UserRepository(model=User, session=self.db_session))
