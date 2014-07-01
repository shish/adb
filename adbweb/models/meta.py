from sqlalchemy import (
    Column, ForeignKey, Index,
    Integer, Float,
    Text, String, Unicode,
    Boolean,
    DateTime,
    LargeBinary,
    func,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
