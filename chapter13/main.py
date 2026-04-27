'''Fantasy acquisition API'''
from fastapi import FastAPI
import onnxruntime as rt # load the models from their files and serve inferences in the API
import numpy as np
from schemas import FantasyAcquisitionFeatures, PredictionOutput # import the Pydantic schemas that we created to define the input and output of the API

api_description = """This API predicts the range of costs to acquire a player in fantasy football

The endpoints are grouped into the following categories:

## Analytics
Get information about health of the API.

## Prediction
Get predictions of player acquisition cost.
"""

# Load the ONNX model
sess_10 = rt.InferenceSession("acquisition_model_10.onnx", providers=["CPUExecutionProvider"]) # load and create an inference session
sess_50 = rt.InferenceSession("acquisition_model_50.onnx", providers=["CPUExecutionProvider"])
sess_90 = rt.InferenceSession("acquisition_model_90.onnx", providers=["CPUExecutionProvider"])

# Get the input and output names of the model
input_name_10 = sess_10.get_inputs()[0].name # get the name of the input features from the session object, to be used when making inferences with the model
label_name_10 = sess_10.get_outputs()[0].name # get the name of the output features from the session object, to be used when making inferences with the model
input_name_50 = sess_50.get_inputs()[0].name
label_name_50 = sess_50.get_outputs()[0].name
input_name_90 = sess_90.get_inputs()[0].name
label_name_90 = sess_90.get_outputs()[0].name

# create the FastAPI app object
app = FastAPI(
    description=api_description,
    title="Fantasy acquisition API",
    version="0.1"
)

# create the health check endpoint
@app.get(
    "/",
    summary="Check to see if the Fantasy acquisition API is running",
    description="""Use this endpoint to check if the API is running. You can also check it first before making other calls to be sure it's running.""",
    response_description="A JSON record with a message in it. If the API is running, the message will say successful.",
    operation_id="v0_health_check",
    tags=["analytics"],
)
def root():
    return {"message": "API health check successful"}

### define the API endpoint that provides the prediction capabilities for users
# define the prediction route
# create POST endpoint at the /predict address
@app.post(
    "/predict/",
    response_model=PredictionOutput, # specify the output schema that we created with Pydantic. Used to generate the OAS file
    summary="Predict the cost of acquiring a player",
    description="""Use this endpoint to predict the range of cost to acquire a player in fantasy football.""",
    response_description="""A JSON record three predicted amounts. Together they give a possible range of acquisition costs for a player.""",
    operation_id="v0_predict",
    tags=["prediction"],
)
def predict(features: FantasyAcquisitionFeatures):
    '''function to be called when a user makes a POST request to the /predict endpoint. '''
    # convert Pydantic model to numpy array to be used as input to the model
    input_data = np.array([[features.waiver_value_tier, features.fantasy_regular_season_weeks_remaining, features.league_budget_pct_remaining]], dtype=np.int64)
    
    # call the ONNX Runtime and get inference results using the input from the API call
    pred_onx_10 = sess_10.run([label_name_10], {input_name_10: input_data})[0]
    pred_onx_50 = sess_50.run([label_name_50], {input_name_50: input_data})[0]
    pred_onx_90 = sess_90.run([label_name_90], {input_name_90: input_data})[0]
    
    # Return prediction as a Pydantic response model
    return PredictionOutput(
        winning_bid_10th_percentile=round(pred_onx_10.item(), 2),
        winning_bid_50th_percentile=round(pred_onx_50.item(), 2),
        winning_bid_90th_percentile=round(pred_onx_90.item(), 2),
    )