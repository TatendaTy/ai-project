'''Pydantic schemas'''
from pydantic import BaseModel

class FantasyAcquisitionFeatures(BaseModel):
    '''Define the input values that users will send to get a prediction from the model.'''
    waiver_value_tier: int
    fantasy_regular_season_weeks_remaining: int
    league_budget_pct_remaining: int
    
class PredictionOutput(BaseModel):
    '''Define the output that will be returned from the model. In this case, we are returning three different predictions'''
    winning_bid_10th_percentile: float
    winning_bid_50th_percentile: float
    winning_bid_90th_percentile: float
