from rich import print  # noqa
import sys
from lib.dataclasses.content import ExtractedContent
from lib.db import session
import json

from lib.models.resource import Resource
from utils import prepare_data

def main(data: dict):

    # gen data
    with session.begin() as transaction:

        # resource = session.query(Resource).first()

        try:
            resource = Resource(name='Test Resource', type='PDF')
            session.add(resource)

            pages, chunk_groups = prepare_data(resource, ExtractedContent(**data))
            print(len(pages), len(chunk_groups))
            resource.pages = pages
            resource.chunk_groups = chunk_groups

            transaction.commit()
        except Exception as e:
            # Rollback the transaction in case of error
            transaction.rollback()
            print(f"Error: {e}")
            raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <json_data>")
        sys.exit(1)
    try:
        with open(sys.argv[1], 'r') as f:
            data = json.loads(f.read())
    except json.JSONDecodeError:
        print("Invalid JSON data")
        sys.exit(1)
    main(data)
    session.close()
