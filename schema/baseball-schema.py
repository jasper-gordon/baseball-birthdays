import graphene
from utils import cnx, Person

class Query(graphene.ObjectType):
    top_home_runs = graphene.List(Person, birth_month=graphene.String(), birth_day=graphene.String())

    def resolve_top_home_runs(parent, info, birth_month, birth_day):
        cursor = cnx.cursor()
        query = f"""
            SELECT people.nameFirst AS FirstName, people.nameLast as LastName, SUM(batting.HR) AS total_home_runs
            FROM people
            JOIN batting ON people.playerID = batting.playerID
            WHERE people.birthMonth = '{birth_month}' AND people.birthDay = '{birth_day}'
            GROUP BY people.playerID
            ORDER BY total_home_runs DESC
            LIMIT 10;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        people = []
        for row in result:
            person = Person(
                id=row[0] + '-' + row[1],
                first_name=row[0],
                last_name=row[1],
                total_home_runs=row[2]
            )
            people.append(person)
        return people

schema = graphene.Schema(query=Query, types=[Person])