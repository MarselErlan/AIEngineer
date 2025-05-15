from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

##create a post endpoint called postApplication() return "message": "Application submitted successfully"

@app.post("/application")
def postApplication():
    return {"message": "Application submitted successfully"}

##Create another POST request called applyForCandidate() -> /application/{candidate_id} return "Application for candidateID: 122 successfully submitted" 

@app.post("/application/{candidate_id}")
def applyForCandidate(candidate_id: int):
    return {f"Application for candidateID: {candidate_id} successfully submitted"}


# add a get request called applicantions it should support query params.
# if the queary params is included in the request return --> "Here is your application for {companyName}"
# if the queary params si not included in the request return --> "Here are all of your applications"

@app.get("/applications")
def get_applications(company_name: str = Query(None, description="optional query param for companyName"), candidate_email: str = Query(None, description="optional query param for candidateEmail")):
    if company_name :
        return {"message": "Here is your application for " + company_name }
    else:
        return {"message": "Here are all of your applications"}
        