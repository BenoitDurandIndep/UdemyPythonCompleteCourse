import re
import string
from tinydb import TinyDB, where
from pathlib import Path


class User:

    DB = TinyDB(Path(__file__).resolve().parent/"db.json", indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return f"{self.full_name}\n{self.phone_number}\n{self.address}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def db_instance(self):
        return User.DB.get((where("first_name") == self.first_name) & (where("last_name") == self.last_name))

    def _checks(self):
        self._check_phone_number
        self._check_names

    def _check_phone_number(self):
        phone_num = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_num) < 10 or not phone_num.isdigit():
            raise ValueError(
                f"Numéro de téléphone {self.phone_number} invalide.")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError(f"Le prénom et le nom ne peuvent pas être vides.")

        spe_characters = string.punctuation + string.digits
        for char in self.full_name:
            if char in spe_characters:
                raise ValueError(f"Le nom n'est pas valide {self.full_name}.")

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()

        if self.exists():
            return -1
        else:
            return User.DB.insert(self.__dict__)

    def exists(self) -> bool:
        return bool(self.db_instance)

    def delete(self) -> list[int]:
        if self.exists():
            # type: ignore
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []


def get_all_users():
    return [User(**user) for user in User.DB.all()]
    # for user in User.DB.all():
    # 	User(**user)


if __name__ == "__main__":
#    get_all_users()
    """     from faker import Faker
        fake = Faker()
        for _ in range(10):
            user = User(first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number(),
                    address=fake.address()
                    )
            print(user)
            print("-"*10)
            user.save()
            print(user.db_instance)
            #user.delete()
        print("$"*10)
    """    
    for user in get_all_users():
        print(user)
