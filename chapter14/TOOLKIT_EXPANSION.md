# SportsWorldCentral Toolkit Expansion

## Overview
The `SportsWorldCentralToolkit` has been expanded from **3 tools** to **7 tools**, providing comprehensive access to the Fantasy Football API endpoints.

## Tools Available

### Original Tools (3)
| # | Tool Name | Method | Purpose | Parameters |
|---|-----------|--------|---------|------------|
| 1 | **HealthCheck** | `get_health_check()` | Verify API is running | None |
| 2 | **ListLeagues** | `list_leagues(league_name)` | Get all leagues | `league_name` (optional) |
| 3 | **ListTeams** | `list_teams(team_name, league_id)` | Get teams with optional filters | `team_name`, `league_id` (both optional) |

### New Tools Added (4)
| # | Tool Name | Method | Purpose | Parameters |
|---|-----------|--------|---------|------------|
| 4 | **GetCounts** | `get_counts()` | Get counts of leagues, teams, players | None |
| 5 | **GetLeagueById** | `get_league_by_id(league_id)` | Get a specific league by ID | `league_id` (required, int) |
| 6 | **ListPlayers** | `list_players(first_name, last_name, position)` | Get players with optional filters | `first_name`, `last_name`, `position` (all optional) |
| 7 | **ListPerformances** | `list_performances(limit)` | Get player performances with fantasy points | `limit` (optional, default=100) |

## Implementation Details

### File Location
- **File**: `/workspaces/ai-project/chapter14/swc_toolkit.py`
- **Lines**: 257 total
- **Structure**: One class per tool + BaseToolkit subclass

### Each Tool Follows This Pattern:
```python
class <ToolName>Input(BaseModel):
    """Pydantic schema for tool input validation"""
    param1: Optional[str] = Field(...)
    param2: Optional[int] = Field(...)

class <ToolName>Tool(BaseTool):
    name: str = "<ToolName>"
    description: str = "Human-readable description for the LLM"
    args_schema: Type[<ToolName>Input] = <ToolName>Input
    
    def _run(self, param1=None, param2=None, run_manager=None):
        result = local_swc_client.<sdk_method>(param1=param1, param2=param2)
        return result
```

### SportsWorldCentralToolkit.get_tools()
```python
return [
    HealthCheckTool(),           # 1. Check API health
    GetCountsTool(),             # 2. Get data counts
    ListLeaguesTool(),           # 3. List leagues
    GetLeagueByIdTool(),         # 4. Get league by ID
    ListTeamsTool(),             # 5. List teams
    ListPlayersTool(),           # 6. List players
    ListPerformancesTool()       # 7. List performances
]
```

## API Data Types
Tools use these Pydantic models imported from `swcpy.swc_client`:
- `League`: League data with id, name, and teams
- `Team`: Team data with id, name, league_id, and players
- `Player`: Player data with id, first_name, last_name, position, nfl_id
- `Performance`: Performance data with player_id, week, fantasy_points

## Testing Results

### Test Date
May 8, 2026

### Environment
- Python: 3.x (venv)
- API Backend: Render (https://fantasyfootball-api-service-lmm2.onrender.com)
- SDK Version: swcpy-tydennis0501

### All 7 Tools Verified ✓
```
1. HealthCheckTool         ✓ PASS
2. GetCountsTool           ✓ PASS
3. ListLeaguesTool         ✓ PASS
4. GetLeagueByIdTool       ✓ PASS
5. ListTeamsTool           ✓ PASS
6. ListPlayersTool         ✓ PASS
7. ListPerformancesTool    ✓ PASS
```

### Sample Data Retrieved
- **Leagues**: Multiple leagues successfully retrieved
- **Teams**: Teams filtered by league_id
- **Players**: Players with position data (QB, RB, WR, TE, K, DEF)
- **Performances**: Fantasy point data for player performances

## Integration with LangGraph Agent

The expanded toolkit can be used in `langgraph_notebook_with_toolkit.ipynb`:

```python
from swc_toolkit import SportsWorldCentralToolkit

toolkit = SportsWorldCentralToolkit()
tools = toolkit.get_tools()

# Bind to NVIDIA model
model_with_tools = model.bind_tools(tools)

# Model can now call any of the 7 tools
# Examples:
# - "What leagues are available?"
# - "Show me all players with position QB"
# - "What are the top 5 recent performances?"
# - "Get league details for league 1"
```

## Usage Examples

### Check API Health
```python
health_tool = toolkit.get_tools()[0]  # HealthCheckTool
result = health_tool._run()
```

### Get Data Counts
```python
counts_tool = toolkit.get_tools()[1]  # GetCountsTool
result = counts_tool._run()
# Returns: Dict with counts of leagues, teams, players, performances
```

### List Players by Position
```python
players_tool = toolkit.get_tools()[5]  # ListPlayersTool
qbs = players_tool._run(position="QB")
# Returns: List[Player] filtered by position
```

### Get Recent Performances
```python
perf_tool = toolkit.get_tools()[6]  # ListPerformancesTool
recent = perf_tool._run(limit=10)
# Returns: Top 10 recent performances with fantasy points
```

## Configuration
- **API URL Source**: Environment variable `SWC_API_BASE_URL` (loaded from `.env`)
- **SDK Client**: `local_swc_client` instantiated with `SWCConfig`
- **Backoff Strategy**: Disabled for immediate responses (`backoff=False`)

## Next Steps

### Optional: Additional Tools (Not Yet Implemented)
The API also provides these endpoints that could be wrapped as tools:
- `get_bulk_player_file()`: Download all players as CSV
- `get_bulk_team_file()`: Download all teams as CSV
- `get_bulk_league_file()`: Download all leagues as CSV
- `get_bulk_performance_file()`: Download all performances as CSV
- `get_bulk_team_player_file()`: Download team-player memberships as CSV

### Testing with Notebook
To test the expanded toolkit in action, run the agent in:
```
/workspaces/ai-project/chapter14/langgraph_notebook_with_toolkit.ipynb
```

The agent can now use all 7 tools to answer questions about the Fantasy Football data.

## File Changes Summary

### Modified Files
- **`/workspaces/ai-project/chapter14/swc_toolkit.py`**
  - Added imports: `Player`, `Performance` from `swcpy.swc_client`
  - Added 4 new tool classes: `GetCountsTool`, `GetLeagueByIdTool`, `ListPlayersTool`, `ListPerformancesTool`
  - Added 4 new input schema classes: `CountsInput`, `LeagueByIdInput`, `PlayersInput`, `PerformancesInput`
  - Updated `SportsWorldCentralToolkit.get_tools()` to include all 7 tools

### No Breaking Changes
- Existing tools (HealthCheck, ListLeagues, ListTeams) maintain backward compatibility
- Same configuration and SDK initialization approach
- All tools follow the same LangChain `BaseTool` pattern
