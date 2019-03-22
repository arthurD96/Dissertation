import sqlite3


def connectToSQL():
    conn = sqlite3.connect('tsp.db')
    cursor = conn.cursor()
    return conn, cursor


def createTable(cursor):
    cursor.execute("""CREATE TABLE tsp (
                    representation text,
                    numberOfCities integer,
                    populationSize integer,
                    childPopulationSize integer,
                    generationGap integer,
                    mutationRate real,
                    algorithm blob PRIMARY KEY ,
                    selection blob,
                    termination blob,
                    cityCoordinates blob,
                    originalSolution blob,
                    finalSolution blob,
                    algorithmEfficiency int
                                        )""")


def checkAlgorithmExists(algorithm, cursor):
    cursor.execute("SELECT * FROM tsp WHERE algorithm = ?", (algorithm,))
    if cursor.fetchone() is None:
        return False
    else:
        return True


def checkForAlgorithmImprovement(row, algorithm, cursor):
    newAlgorithmEfficiency = int(row[12])
    cursor.execute("SELECT algorithmEfficiency FROM tsp WHERE algorithm = ?", (algorithm,))
    existingAlgorithmEfficiency = cursor.fetchone()[0]
    if existingAlgorithmEfficiency < newAlgorithmEfficiency:
        return True
    else:
        return False


def insertResults(results, cursor):
    cursor.execute("INSERT INTO tsp VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7],
        results[8], results[9], results[10], results[11], results[12]))


def replaceResults(results, cursor):
    values = results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7], \
             results[8], results[9], results[10], results[11], results[12]
    replaceQuery = """
            REPLACE INTO tsp (
            representation, numberOfCities, populationSize, childPopulationSize, generationGap, mutationRate, algorithm,
            selection, termination, cityCoordinates, originalSolution, finalSolution, algorithmEfficiency)
            VALUES"""
    replaceQuery += str(values)
    cursor.execute(replaceQuery)


def disconnectFromSQL(conn):
    conn.commit()
    conn.close()
