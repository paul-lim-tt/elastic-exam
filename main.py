from rich import print  # noqa
from lib.db import session

from lib.models.resource import Resource

def main():
    resource = session.query(Resource).first()
    pages = resource.pages
    chunk_groups = resource.chunk_groups
    print(pages[0].__dict__)
    print(chunk_groups[0].__dict__)


if __name__ == "__main__":
    main()