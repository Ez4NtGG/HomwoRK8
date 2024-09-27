from pathlib import Path
import json
from faker import Faker
from tqdm import tqdm

from hw08.database.models import Authors, Quotes, Contacts, PreferTypes


def load_json_files_from_dir(json_dir: Path) -> dict:
    result = {}
    if json_dir.exists():
        for file_item in json_dir.glob("*.json"):
            if file_item.is_file():
                with file_item.open("r", encoding="UTF-8") as fp:
                    result[file_item.stem] = json.load(fp)
    return result


def seeds(debug: bool = False):
    json_dir = Path(__file__).parent.joinpath("json")
    json_dict = load_json_files_from_dir(json_dir)

    if not json_dict:
        print("Files JSON not found")
        return 1

    authors_id = {}
    seed_object = "authors"
    print(f"Add {seed_object}...")
    if seed_object in json_dict:
        Authors.drop_collection()
        so = json_dict.get(seed_object)
        for author in tqdm(so, total=len(so)):
            rec = Authors(**author).save()
            authors_id[author.get("fullname")] = rec.id

    seed_object = "quotes"
    print(f"Add {seed_object}...")
    if seed_object in json_dict:
        Quotes.drop_collection()
        so = json_dict.get(seed_object)
        for quote in tqdm(so, total=len(so)):
            author = quote.get("author")
            author_id = authors_id.get(author)
            if author_id:
                quote["author"] = author_id
                rec = Quotes(**quote).save()
                author_by_id = Authors.objects(id=author_id).first()

    if debug:
        authors = Authors.objects()
        for record in authors:
            print("-------------------")
            print(record.to_mongo().to_dict())

        quotes = Quotes.objects()
        for record in quotes:
            print("-------------------")
            print(record.to_mongo().to_dict())


        find1 = Authors.objects(fullname="Steve Martin").delete()
        print("deleted", find1)

        find1 = Authors.objects()
        for record in find1:
            print("-------------------")
            print(record.to_mongo().to_dict())


def seed_prefer_types() -> list[str]:
    result = {
        "type_sms": PreferTypes(type="SMS"),
        "type_email": PreferTypes(type="EMAIL"),
    }
    return result


def seed_contacts(max_records: int = 100, preffer_type: str = "type_email", drop: bool = True) -> list[str]:

    fake = Faker("uk-UA")
    types=seed_prefer_types()

    print(f"Add contacts: {max_records} ...")
    if drop:
        Contacts.drop_collection()
    result = []
    for i in tqdm(range(max_records)):
        obj = {
            "fullname": " ".join([fake.first_name(), fake.last_name()]),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "birthday": fake.date_between(),
            "prefer": types.get(preffer_type)
        }
        contact = Contacts(**obj).save()
        obj_id = contact.id
        result.append(str(obj_id))
    return result

if __name__ == "__main__":
    from hw08.database.connect import connect_db

    if connect_db():
        print(seed_contacts(10))
