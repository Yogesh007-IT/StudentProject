import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from pydantic import BaseModel

from starlette.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

VALID_USERNAME = "vebbox"
VALID_PASSWORD = "12345"

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != VALID_USERNAME or credentials.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username






class Item(BaseModel):
    username: str
    password: str

def get_db_connection():
    return mysql.connector.connect(
        host="m8q01.h.filess.io",
        user="yogesh_unionswing",
        password="a2a4bf471e9c19b82b19f3e0eafde80eafd0f29f",
        database="yogesh_unionswing",
        port="3307"
    )

class Item (BaseModel) :
    username:str
    age:str
    phoNo:str
    email:str
    course:str

@app.get("/studentDetail")
def get_Students():
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)  # Get results as dictionary

        cursor.execute("SELECT * FROM onepiece")
        students = cursor.fetchall()

        cursor.close()
        mydb.close()

        return students

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/insertDetail")
def post_details(obj : Item):
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()

        query="""Insert into onepiece (username,age,phoneno,email,course) values (%s,%s,%s,%s,%s)"""
        values=(obj.username,obj.age,obj.phoNo,obj.email,obj.course)

        cursor.execute(query, values)
        mydb.commit()
        student_id = cursor.lastrowid  # Get inserted student ID
        cursor.close()
        mydb.close()

        return {"message": "Student added successfully", "student_id": student_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class DeleteRequest(BaseModel):
    id: int

@app.post("/Delete")
def post_details(o: DeleteRequest):
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()

        cursor.execute("DELETE FROM onepiece WHERE S_NO = %s", (o.id,))
        mydb.commit()

        cursor.close()
        mydb.close()

        return {"message": "Student deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



@app.get("/getDetail/{id}")
def get_detail(id : int):
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)  # Get results as dictionary

        cursor.execute("SELECT * FROM onepiece where S_NO=%s",(id,))
        students = cursor.fetchall()

        cursor.close()
        mydb.close()

        return students

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")




class UpdateFieldRequest(BaseModel):
    field: str
    value: str


@app.patch("/updateField/{id}")
def update_field(id: int, data: UpdateFieldRequest):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        allowed_fields = ["username", "age", "phoneno", "email", "course"]
        if data.field not in allowed_fields:
            raise HTTPException(status_code=400, detail=f"Field '{data.field}' is not allowed to update.")

        sql = f"UPDATE onepiece SET {data.field} = %s WHERE S_NO = %s"
        cursor.execute(sql, (data.value, id))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")

        return {"message": f"{data.field} updated successfully!"}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        connection.close()
