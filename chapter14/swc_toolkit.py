import os
from typing import Optional, Type, List
from swcpy import SWCConfig, SWCClient
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# langchain library for defining tools and toolkits
from langchain_core.callbacks import CallbackManagerForToolRun 
from langchain_core.tools import BaseTool, BaseToolkit

# check to see if the swc SDK has been installed in the environment
try:
    from swcpy import SWCClient
    from swcpy.swc_client import League, Team
except ImportError:
    raise ImportError(
        "swcpy is not installed. Please install it."
    )

load_dotenv(override=True)

def resolve_swc_base_url() -> str:
    """Resolve the SWC API URL from the environment."""
    swc_base_url = os.environ.get("SWC_API_BASE_URL")
    if not swc_base_url:
        raise ValueError(
            "SWC_API_BASE_URL is not set. Add the Render or Azure deployment URL to chapter14/.env."
        )
    return swc_base_url


swc_base_url = resolve_swc_base_url()
os.environ["SWC_API_BASE_URL"] = swc_base_url

config = SWCConfig(swc_base_url=swc_base_url, backoff=False) # instantiate the SDK
local_swc_client = SWCClient(config)

class HealthCheckInput(BaseModel):
    """for each tool, define an input schema/object that inherits from pydantic BaseModel."""    
    pass

class HealthCheckTool(BaseTool):
    """a tool that checks if the API is running. Information provided is used by the model to decide how and when to use this tool."""    
    name: str = "HealthCheck"
    description: str = (
        "useful to check if the API is running before you make other calls"
    )
    args_schema: Type[HealthCheckInput] = HealthCheckInput # define the expected inputs, and send input to the tool
    return_direct: bool = False
    
    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to check if the API is running."""
        health_check_response = local_swc_client.get_health_check() # make the API call using the SDK client
        return health_check_response.text

class LeaguesInput(BaseModel):
    """input defined for the ListLeaguesTool. Contains parameters used by the tool

    Args:
        BaseModel (List[League]) : inherits from pydantic BaseModel, which allows for data validation and parsing.
    """    
    league_name: Optional[str] = Field(
        default=None, 
        description="league name. Leave blank or None to get all leagues."
    )
    
class ListLeaguesTool(BaseTool):
    """The tool that will be used to call the SDK's list_leagues() function

    Args:
        BaseTool: inherits from langchain_core's BaseTool, which allows us to define a tool that can be used by the model. We need to define the name, description, args_schema, and return_direct attributes, as well as the _run() method that contains the logic for calling the SDK function.

    Returns:
        List[League]: A list of leagues from SportsWorldCentral.
    """    
    name: str = "ListLeagues"
    description: str = (
        "get a list of leagues from SportsWorldCentral. "
        "Leagues contain teams if they are present."
    )
    args_schema: Type[LeaguesInput] = LeaguesInput
    return_direct: bool = False
    
    def _run(
        self, league_name: Optional[str] = None, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[League]:
        """Use the tool to get a list of leagues from SportsWorldCentral."""
        # Call the API with league_name, which could be None
        list_leagues_response = local_swc_client.list_leagues(league_name=league_name)
        return list_leagues_response
    
class TeamsInput(BaseModel):
    """this class defines the input schema for the ListTeamsTool.
    It contains parameters that can be used to filter the teams that are returned by the tool.
    The parameters are optional, and if they are not provided, the tool will return all teams.   
    """
    team_name: Optional[str] = Field(
        default=None, 
        description="Name of the team to search for. Leave blank or None to get all teams.")
    league_id: Optional[int] = Field(
        default=None,
        description=(
            "League ID from a league. You must provide a numerical League ID."
            "Leave blank or None to get teams from all leagues."
            ))

class ListTeamsTool(BaseTool):
    """The tool that will be used to call the SDK's list_teams() function with optional parameters for team name and league ID."""
    name: str = "ListTeams"
    description: str = (
        "Get a list of teams from SportsWorldCentral. Teams contain players "
        "if they are present. Optionally provide a numerical League ID to "
        "filter teams from a specific league.")
    args_schema: Type[TeamsInput] = TeamsInput # define the expected inputs, and send input to the tool
    return_direct: bool = False
    
    def _run(
        self, team_name: Optional[str] = None,
        league_id: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Team]:
        """Use the tool to get a list of teams from SportsWorldCentral."""
        # Call the API with team_name and league_id, which could be None
        list_teams_response = local_swc_client.list_teams(
            team_name=team_name,
            league_id=league_id)
        return list_teams_response

class SportsWorldCentralToolkit(BaseToolkit):
    """subclass of BaseToolkit that defines the tools that will be used by the model. The get_tools() method returns a list of the tools that we have defined above."""
    def get_tools(self) -> List[BaseTool]:
        '''Return the list of tools in the toolkit.'''
        return [
            HealthCheckTool(),
            ListLeaguesTool(),
            ListTeamsTool()
        ] # instatiate the tools and return them in a list


