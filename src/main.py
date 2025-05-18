from fastapi import FastAPI, Query, Request, Path, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

applications_db = {}

# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# ##create a post endpoint called postApplication() return "message": "Application submitted successfully"

# @app.post("/application")
# def postApplication():
#     return {"message": "Application submitted successfully"}

# ##Create another POST request called applyForCandidate() -> /application/{candidate_id} return "Application for candidateID: 122 successfully submitted" 

# @app.post("/application/{candidate_id}")
# def applyForCandidate(candidate_id: int):
#     return {f"Application for candidateID: {candidate_id} successfully submitted"}


# # add a get request called applicantions it should support query params.
# # if the queary params is included in the request return --> "Here is your application for {companyName}"
# # if the queary params si not included in the request return --> "Here are all of your applications"

# @app.get("/applications")
# def get_applications(company_name: str = Query(None, description="optional query param for companyName"), candidate_email: str = Query(None, description="optional query param for candidateEmail")):
#     if company_name :
#         return {"message": "Here is your application for " + company_name }
#     else:
#         return {"message": "Here are all of your applications"}
        

class Application(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_id: str
    company_name: Optional[str] = None
    candidate_email: Optional[str] = None

class ApplicationPartialUpdate(BaseModel):
    email: Optional[str] = None
    job_id: Optional[str] = None

@app.post("/applicationshw")
def submit_application(app: Application):
    applications_db[app.candidate_id] = app.dict()
    return {
        "status": "success",
        "message": f"Application submitted for {app.name}"
    }

@app.get("/applicationshw")
def get_applications(
    company_name: str = Query(None, description="optional query param for companyName"), 
    candidate_email: str = Query(None, description="optional query param for candidateEmail")
):
    messages = []

    if company_name:
        messages.append(f"Here is your application for company: {company_name}")
        
    if candidate_email:
        messages.append(f"Here is your application for email: {candidate_email}")

    if messages:
        return {
            "status": "success",
            "message": messages
        }
    
    return {
        "status": "success",
        "message": "Here are all of your applications",
        "data": applications_db
    }

@app.get("/applicationshw/{candidate_id}")
def get_with_candidate_id(candidate_id: str):
    if candidate_id not in applications_db:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "status": "success",
        "message": f"Application found for candidate ID: {candidate_id}",
        "data": applications_db[candidate_id]
    }

@app.put("/applicationshw/{candidate_id}")
def update_applications(candidate_id: str, app: Application):
    if candidate_id not in applications_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    applications_db[candidate_id] = app.dict()
    return {
        "status": "success",
        "message": f"Application for {candidate_id} successfully updated",
        "data": applications_db[candidate_id]
    }

@app.patch("/applicationshw/{candidate_id}")
def patch_application(candidate_id: str, update: ApplicationPartialUpdate):
    if candidate_id not in applications_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    existing = applications_db[candidate_id]
    update_data = update.dict(exclude_unset=True)
    existing.update(update_data)
    applications_db[candidate_id] = existing
    return {
        "status": "success",
        "message": f"Application for {candidate_id} successfully updated with fields: {list(update_data.keys())}",
        "data": applications_db[candidate_id]
    }

@app.delete("/applicationshw/{candidate_id}")
def delete_application(candidate_id: str):
    if candidate_id not in applications_db:
        raise HTTPException(status_code=404, detail="Candidate not found")
    deleted_data = applications_db.pop(candidate_id)
    return {
        "status": "success",
        "message": f"Application for {candidate_id} has been deleted",
        "data": deleted_data
    }



