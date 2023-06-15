from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
engine = create_engine("sqlite:///test.db", echo=True, future=True)
# engine = create_engine("postgresql://scott:tiger@localhost/test")
# engine = create_engine("mysql://scott:tiger@hostname/dbname", encoding='latin1', echo=True)

# engine.execution_options(isolation_level="AUTOCOMMIT")  # setting to autocommit

'''
- What kind of database are we communicating with? This is the sqlite portion above
- What DBAPI are we using? The Python DBAPI is a third party driver that SQLAlchemy uses to interact with a particular 
database. In this case, we're using the name pysqlite, which in modern Python use is the sqlite3 standard library 
interface for SQLite.
- How do we locate the database? In this case, our URL includes the phrase /:memory:, which is an indicator to the 
sqlite3 module that we will be using an in-memory-only database.
- echo=True says that the standard output will be logged on the terminal
- future=True ensures that the latest version of SQLAlchemy engine 2.0 is used
'''

# with engine.connect() as conn:
#     result = conn.execute(text("select \"hello world\""))  # Blank command :)
#     print(result.all())
#
# # Commit as you go
# with engine.connect() as conn:
#     conn.execute(text(
#         "CREATE TABLE IF NOT EXISTS TEST("
#         "X INT,"
#         "Y INT"
#         ")"''
#     ))
#     conn.execute(
#         text("INSERT INTO TEST VALUES(:x, :y);"),
#         [{"x": 1, "y": 2}, {"x": 2, "y": 4}]
#     )  # Not committed
#
#     # conn.commit()  # Not working :(
#
# # Begin once
# with engine.begin() as conn:
#     conn.execute(text(
#         "INSERT INTO TEST VALUES(:x, :y);"), [{"x": i, "y": i*2} for i in range(1, 7)]
#         #                                    ↑↑↑↑↑↑↑→ sending multiple parameters  ↓←
#     )  # Committed :)
#
# # Fetch data
# with engine.connect() as conn:
#     result = conn.execute(text(
#         "SELECT X, Y FROM TEST"
#     ))
#     for row in result:
#         '''
#         The elements can be accessed via
#         1. for x, y in result: ...
#         2. for row in result: x = row[0]; y = row[1]; ...
#         3. for row in result: x = row.x; y = row.y; ...
#         4. for dct in result.mappings(): x = dct['x']; y = dct['y']; ...
#         '''
#         print(row[0], row[1])
#
# # Sending parameters
# with engine.connect() as conn:
#     result = conn.execute(
#         text("SELECT X, Y FROM TEST where Y > :y"),
#         {"y": 2}
#     )
#     for row in result:
#         print(row)

'''
The fundamental transactional / database interactive object when using the ORM is called the Session. In modern 
SQLAlchemy, this object is used in a manner very similar to that of the Connection, and in fact as the Session is used, 
it refers to a Connection internally which it uses to emit SQL.
The Session doesn't actually hold onto the Connection object after it ends the transaction. It gets a new Connection 
from the Engine when executing SQL against the database is next needed.
'''
stmt = text("SELECT X, Y FROM TEST WHERE Y > :Y ORDER BY X, Y").bindparams(Y=6)
# stmt = text("INSERT INTO TEST (Y, X) VALUES (12, 6)")  # Doesn't commit
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(row)

Session2 = sessionmaker(engine)
# No need to pass engine to session after using sessionmaker
with Session2() as session:
    # Or can be used as Session2.begin/commit/rollback()
    result = session.execute(
        text("UPDATE TEST SET Y=:y WHERE X=:x"),
        [{"x": i, "y": i*3} for i in range(0, 7, 3)]  # Just change the Y value of multiples of 3
    )
    r = session.execute(text("SELECT X, Y FROM TEST WHERE Y > :Y ORDER BY X, Y").bindparams(Y=6))
    for row in r:
        print(row)
