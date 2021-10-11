from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import re

app = FastAPI()

#  Class that inherits from BaseModel to create the User
class User(BaseModel):
    email: str
    password: str

# Dictionary with credentials to validate
pierre_creds = {"email":"pierre@palenca.com", 
                "password":"MyPwdChingon123"}

# Regular expression for validating an email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@app.get("/")
def hello_palenca():
	return "Hello Palenca"


@app.post("/uber/login")
def uber_login(user: User):
    
    # The correct format of the email is checked
    if not re.fullmatch(regex, user.email):
        raise HTTPException(status_code = 401,
                            detail = {"message": "CREDENTIALS_INVALID",
                                      "details": "The email format is invalid"})
    # The length of the password is checked
    if len(user.password) <= 5:
        raise HTTPException(status_code = 401,
                            detail = {"message": "CREDENTIALS_INVALID",
                                      "details": "Passwords must have more than 5 characters"})                                  
    if not (user.email == pierre_creds["email"]) | (user.password == pierre_creds["password"]):
        raise HTTPException(status_code = 401,
                            detail = {"message": "CREDENTIALS_INVALID",
                                      "details": "Incorrect username or password"})
    return 200,{"message":"SUCCESS",
                "access_token":"cTV0aWFuQ2NqaURGRE82UmZXNVBpdTRxakx3V1F5"}


@app.get("/uber/get-profile/{access_token}")
def get_profile(access_token: str = Path(..., description = "The access token of the user.")):
    if access_token != 'cTV0aWFuQ2NqaURGRE82UmZXNVBpdTRxakx3V1F5':
        raise HTTPException(status_code = 401,
                            detail={"message": "CREDENTIALS_INVALID",
                                     "detail": "Incorrect token"})
                            
    return 200,{"message": "SUCCESS",
                "platform": "uber",
                "profile": {
                    "country": "mx",
                    "city_name": "Ciudad de Mexico",
                    "worker_id": "34dc0c89b16fd170eba320ab186d08ed",
                    "first_name": "Pierre",
                    "last_name": "Delarroqua",
                    "email": "pierre@palenca.com",
                    "phone_prefix": "+52",
                    "phone_number": "5576955981",
                    "rating": "4.8",
                    "lifetime_trips": 1254
                }
                }
