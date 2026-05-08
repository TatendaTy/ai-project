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
    from swcpy.swc_client import League, Team, Player, Performance
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

class CountsInput(BaseModel):
    """Input for the GetCountsTool. Contains no required parameters."""
    pass

class GetCountsTool(BaseTool):
    """The tool that will be used to call the SDK's get_counts() function."""
    name: str = "GetCounts"
    description: str = (
        "Get counts of leagues, teams, and players from SportsWorldCentral. "
        "Useful for understanding the size and scope of the available data."
    )
    args_schema: Type[CountsInput] = CountsInput
    return_direct: bool = False
    
    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to get counts of data from SportsWorldCentral."""
        counts_response = local_swc_client.get_counts()
        return str(counts_response)

class PlayersInput(BaseModel):
    """Input for the ListPlayersTool. Contains optional player filter parameters."""
    first_name: Optional[str] = Field(
        default=None,
        description="First name of the player to search for."
    )
    last_name: Optional[str] = Field(
        default=None,
        description="Last name of the player to search for."
    )
    position: Optional[str] = Field(
        default=None,
        description="Position of the player (e.g., QB, RB, WR, TE, K, DEF)."
    )

class ListPlayersTool(BaseTool):
    """The tool that will be used to call the SDK's list_players() function."""
    name: str = "ListPlayers"
    description: str = (
        "Get a list of NFL players from SportsWorldCentral. "
        "Optionally filter by first name, last name, or position."
    )
    args_schema: Type[PlayersInput] = PlayersInput
    return_direct: bool = False
    
    def _run(
        self, first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        position: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Player]:
        """Use the tool to get a list of players from SportsWorldCentral."""
        list_players_response = local_swc_client.list_players(
            first_name=first_name,
            last_name=last_name,
            position=position
        )
        return list_players_response

class PerformancesInput(BaseModel):
    """Input for the ListPerformancesTool. Contains optional limit."""
    limit: Optional[int] = Field(
        default=100,
        description="Limit the number of results returned. Default is 100."
    )

class ListPerformancesTool(BaseTool):
    """The tool that will be used to call the SDK's list_performances() function."""
    name: str = "ListPerformances"
    description: str = (
        "Get a list of NFL player performances with fantasy points from SportsWorldCentral. "
        "Optionally limit the number of results."
    )
    args_schema: Type[PerformancesInput] = PerformancesInput
    return_direct: bool = False
    
    def _run(
        self, limit: Optional[int] = 100,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Performance]:
        """Use the tool to get performances from SportsWorldCentral."""
        performances_response = local_swc_client.list_performances(
            limit=limit
        )
        return performances_response

class LeagueByIdInput(BaseModel):
    """Input for the GetLeagueByIdTool. Requires a league ID."""
    league_id: int = Field(
        description="The numerical ID of the league to retrieve."
    )

class GetLeagueByIdTool(BaseTool):
    """The tool that will be used to call the SDK's get_league_by_id() function."""
    name: str = "GetLeagueById"
    description: str = (
        "Get a specific league by its ID from SportsWorldCentral. "
        "Requires a numerical league ID."
    )
    args_schema: Type[LeagueByIdInput] = LeagueByIdInput
    return_direct: bool = False
    
    def _run(
        self, league_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> League:
        """Use the tool to get a specific league by ID from SportsWorldCentral."""
        league_response = local_swc_client.get_league_by_id(league_id=league_id)
        return league_response

class SportsWorldCentralToolkit(BaseToolkit):
    """subclass of BaseToolkit that defines the tools that will be used by the model. The get_tools() method returns a list of the tools that we have defined above."""
    def get_tools(self) -> List[BaseTool]:
        '''Return the list of tools in the toolkit.'''
        return [
            HealthCheckTool(),
            GetCountsTool(),
            ListLeaguesTool(),
            GetLeagueByIdTool(),
            ListTeamsTool(),
            ListPlayersTool(),
            ListPerformancesTool()
        ] # instantiate the tools and return them in a list


