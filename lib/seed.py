#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Freebie, Company, Dev, Base

# Create an engine and bind it to the session
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the tables
Base.metadata.create_all(engine)

# Seed data
dev1 = Dev(name='John')
dev2 = Dev(name='Sarah')
dev3 = Dev(name='Michael')

company1 = Company(name='Company A', founding_year=1990)
company2 = Company(name='Company B', founding_year=2005)
company3 = Company(name='Company C', founding_year=2012)

freebie1 = Freebie(item_name='Item 1', value=10, dev=dev1, company=company1)
freebie2 = Freebie(item_name='Item 2', value=20, dev=dev2, company=company1)
freebie3 = Freebie(item_name='Item 3', value=15, dev=dev3, company=company2)

# Add the objects to the session
session.add_all([dev1, dev2, dev3, company1, company2, company3, freebie1, freebie2, freebie3])

# Commit the session to persist the data in the database
session.commit()

# Close the session
session.close()
