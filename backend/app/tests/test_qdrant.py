from vector_store import client, create_collection, COLLECTION_NAME

print("Qdrant collections before:")
print(client.get_collections())

create_collection()

print("\n Qdrant collections after: \n", client.get_collections())