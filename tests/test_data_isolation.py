import pytest
from app.database import File
 
def test_file_requires_owner_id(session):
    f = File(
        original_filename="a.txt",
        stored_filename="a.txt",
        size_bytes=10
    )
    session.add(f)
 
    with pytest.raises(Exception):
        session.commit()