from faker import Faker
from faker.providers import internet, misc, person
from utils.structures import Permission, Role, User

fake = Faker(locale="ru_RU")
fake.add_provider(person)
fake.add_provider(internet)
fake.add_provider(misc)

Faker.seed(0)


class Testdata:
    def gen_user(self, number: int = 100) -> User:

        return User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.free_email(),
            password=fake.password(),
        )

    def gen_role(self) -> Role:
        return Role(name="Роль №{0}".format(fake.uuid4()))

    def gen_permission(self, number: int = 10) -> Permission:
        return Permission(name="Разрешение №{0}".format(fake.uuid4()))
