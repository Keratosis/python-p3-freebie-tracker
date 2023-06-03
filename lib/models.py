from sqlalchemy import ForeignKey, Column, Integer, String, MetaData,Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

dev_company_association = Table(
    'dev_company_association',
    Base.metadata,
    Column('dev_id', Integer, ForeignKey('devs.id')),
    Column('company_id', Integer, ForeignKey('companies.id'))
)

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    companies = relationship('Company', secondary=dev_company_association, backref=backref('dev', uselist=False))

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer())
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship('Dev', backref=backref('freebies', cascade='all, delete-orphan'))
    company = relationship('Company', backref=backref('freebies', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Freebie {self.id}, {self.item_name}, {self.value}, {self.dev_id}, {self.company_id}>'

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(dev=dev, item_name=item_name, value=value)
        self.freebies.append(freebie)

    @classmethod
    def oldest_company(cls):
        return cls.query.order_by(cls.founding_year).first()