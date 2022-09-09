#!/usr/bin/python
import psycopg2
from psycopg2.extras import execute_values


ESLINT_7_ID = -1
ESLINT_7_NAME = 'ESLint (deprecated)'
ESLINT_7_PREFIX = 'ESLint_'
ESLINT_8_ID = -1
ESLINT_8_NAME = 'ESLint'
ESLINT_8_PREFIX = 'ESLint8_'




connection = psycopg2.connect(
    host="localhost",
    database="analysis",
    user="#####",
    password="#####")

def list_eslint7_active_patterns():
    patterns = []
    cursor = connection.cursor()
    query = 'select pp."projectId", p."id", p."internalId", p."title", pp."parameters" from "ProjectPattern" as pp INNER JOIN "Pattern" as p ON (pp."patternId" = p."id") WHERE p."algorithmId" = %s'
    cursor.execute(query,(ESLINT_7_ID,))
    records = cursor.fetchall()
    for record in records:
        patterns.append({
            "projectId": record[0],
            "internalId": record[2].replace(ESLINT_7_PREFIX,''),
            "title": record[3],
            "parameters": record[4]
        })
    return patterns

def list_eslint8_patterns():
    patterns = []
    cursor = connection.cursor()
    query = 'select "id", "internalId", "title", "algorithmId" from "Pattern" where "algorithmId"=%s'
    cursor.execute(query,(ESLINT_8_ID,))
    records = cursor.fetchall()
    for record in records:
        patterns.append({
            "id": record[0],
            "internalId": record[1].replace(ESLINT_8_PREFIX,''),
            "title": record[2],
            "algorithmId": record[3],
        })
    return patterns


def delete_eslint8_active_patterns():
    cursor = connection.cursor()
    query = 'DELETE FROM "ProjectPattern" WHERE "patternId" IN (select "id" from "Pattern" where "algorithmId"=%s)'
    cursor.execute(query,(ESLINT_8_ID,))

def enable_eslint8_patterns(values):
    cursor = connection.cursor()
    query = 'INSERT INTO "ProjectPattern"("patternId", parameters, "projectId") VALUES %s'
    execute_values(cursor, query, (values))



def set_eslint_ids():
    global ESLINT_7_ID, ESLINT_8_ID
    cursor = connection.cursor()
    postgreSQL_select_Query = 'SELECT id,name FROM "Algorithm" WHERE name LIKE \'%ESLint%\''

    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()

    for row in records:
        if row[1] == ESLINT_7_NAME:
            ESLINT_7_ID = row[0]
        elif row[1] == ESLINT_8_NAME:
            ESLINT_8_ID = row[0]


def first(iterable, default=None):
  for item in iterable:
    return item
  return default

def main():
    print("ESLint 7 to 8 patterns migrator")
    set_eslint_ids()
    eslint8_patterns = list_eslint8_patterns()
    eslint7_active_patterns = list_eslint7_active_patterns()
    #print(eslint7_active_patterns)
    eslint8_patterns_to_enable = []
    for pattern in eslint7_active_patterns:
        eslint8_equivalent = first([x["id"] for x in eslint8_patterns if x["internalId"] == pattern["internalId"] ])
        if eslint8_equivalent is not None:
            eslint8_patterns_to_enable.append((eslint8_equivalent, pattern['parameters'], pattern['projectId']))
    delete_eslint8_active_patterns()
    enable_eslint8_patterns(eslint8_patterns_to_enable)
    connection.commit()


main()