import pyodbc
import sqlite3
import os.path

cursor = None
connected_to_sqllite = False


def connect_with_database():
    global cursor

    try:
        connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=(LocalDb)\\MSSQLLocalDB;PORT=1433;Database=Pathfinder_LOCAL;Trusted_Connection=yes;')      
    except :
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, r"databases\PathfinderDB.db")
        connection = sqlite3.connect(db_path)
        global connected_to_sqllite
        connected_to_sqllite= True
 
    cursor = connection.cursor()

def get_position_queries():

    if connected_to_sqllite:
        table = '"dbo.Positions"'
    else:
        table = '[dbo].[Positions]'

    return 'SELECT x,y FROM '+table+' order by x, y'

def get_source_and_target_positions():

    if connected_to_sqllite:
        edges_table = '"dbo.Edges"'
        nodes_table = '"dbo.Nodes"'
        positions_table = '"dbo.Positions"'
    else:
        edges_table = '[dbo].[Edges]'
        nodes_table = '[dbo].[Nodes]'
        positions_table = '[dbo].[Positions]'


    return """SELECT SourcePositions.X as sourceX,SourcePositions.Y as sourceY ,TargetPositions.X as targetX ,TargetPositions.Y as targetY
  FROM """+edges_table+""" as Edges
  join """+nodes_table+""" as SourceNode on SourceNode.Id = Edges.SourceId
  join """+nodes_table+""" as TargetNode on TargetNode.Id = Edges.TargetId
  join """+positions_table+""" as SourcePositions on SourcePositions.Id = SourceNode.PositionId
  join """+positions_table+""" as TargetPositions on TargetPositions.Id = TargetNode.PositionId"""

def get_positions():    
    cursor.execute(get_position_queries())
    return cursor.fetchall()

def get_source_and_targets():
    cursor.execute(get_source_and_target_positions())
    return cursor.fetchall()