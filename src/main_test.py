import sys
import pymongo


try:
    from hw08.database.init import client
except ImportError:
    from src.hw08.database.init import client

if __name__ == "__main__":
    db = client.myDatabase
    my_collection = db["recipes"]
    recipe_documents = [{ "name": "elotes", "ingredients": ["corn", "mayonnaise", "cotija cheese", "sour cream", "lime"], "prep_time": 35 },
                    { "name": "loco moco", "ingredients": ["ground beef", "butter", "onion", "egg", "bread bun", "mushrooms"], "prep_time": 54 },
                    { "name": "patatas bravas", "ingredients": ["potato", "tomato", "olive oil", "onion", "garlic", "paprika"], "prep_time": 80 },
                    { "name": "fried rice", "ingredients": ["rice", "soy sauce", "egg", "onion", "pea", "carrot", "sesame oil"], "prep_time": 40 }]
    
    try:
        my_collection.drop()  

    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are your username and password correct in your connection string?")

    
    try: 
        result = my_collection.insert_many(recipe_documents)

    except pymongo.errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
    else:
        inserted_count = len(result.inserted_ids)
        print("I inserted %x documents." %(inserted_count))

        print("\n")


    result = my_collection.find()

    if result:    
        for doc in result:
            my_recipe = doc['name']
            my_ingredient_count = len(doc['ingredients'])
            my_prep_time = doc['prep_time']
            print("%s has %x ingredients and takes %x minutes to make." %(my_recipe, my_ingredient_count, my_prep_time))
            
    else:
        print("No documents found.")

        print("\n")

    my_doc = my_collection.find_one({"ingredients": "potato"})

    if my_doc is not None:
        print("A recipe which uses potato:")
        print(my_doc)
    else:
        print("I didn't find any recipes that contain 'potato' as an ingredient.")
        print("\n")

    my_doc = my_collection.find_one_and_update({"ingredients": "potato"}, {"$set": { "prep_time": 72 }}, new=True)
    if my_doc is not None:
        print("Here's the updated recipe:")
        print(my_doc)
    else:
        print("I didn't find any recipes that contain 'potato' as an ingredient.")
        print("\n")

    my_result = my_collection.delete_many({ "$or": [{ "name": "elotes" }, { "name": "fried rice" }]})
    print("I deleted %x records." %(my_result.deleted_count))
    print("\n")
