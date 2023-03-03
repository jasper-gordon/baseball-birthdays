import mysql.connector
import graphene
import os

# Define a connection to the MySQL database
cnx = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_DATABASE']
)

# Define a GraphQL object type for a Person
class Person(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    total_home_runs = graphene.Int()
