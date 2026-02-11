# import pytest
# from app.database import File
 
# def test_file_requires_owner_id(session):
#     f = File(
#         original_filename="a.txt",
#         stored_filename="a.txt",
#         size_bytes=10
#     )
#     session.add(f)
 
#     with pytest.raises(Exception):
#         session.commit()




import pytest
from sqlalchemy.exc import IntegrityError
from app.database import File


def test_file_requires_owner_id(session):
    f = File(
        original_filename="a.txt",
        stored_filename="a.txt",
        size_bytes=10,
        # owner_id missing on purpose
    )
    session.add(f)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()
