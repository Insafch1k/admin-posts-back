from sqlalchemy import Table, Column, Integer, ForeignKey
from ..database import Base

# Many-to-Many: Source <-> Tag
sourcetag_table = Table(
    'sourcetag',
    Base.metadata,
    Column('source_id', Integer, ForeignKey('sources.source_id')),
    Column('tag_id', Integer, ForeignKey('tags.tag_id'))
)