from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from graph.workflow import graph

app = FastAPI()


class GenerateRequest(BaseModel):
    topic: str


@app.post("/generate")
def generate(topic: str = None, request: GenerateRequest = None):
    """Generate content for a given topic with error handling
    
    Accepts either:
    - Query parameter: POST /generate?topic=your_topic
    - JSON body: POST /generate with {"topic": "your_topic"}
    """
    try:
        # Use query parameter if provided, otherwise use request body
        actual_topic = topic or (request.topic if request else None)
        
        if not actual_topic:
            raise HTTPException(
                status_code=400,
                detail="Topic is required. Use ?topic=... or provide JSON body"
            )
        
        result = graph.invoke(
            {
                "topic": actual_topic
            }
        )
        return {
            "status": "success",
            "result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error during generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content: {str(e)}"
        )


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}