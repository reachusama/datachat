from typing import Optional, Type, TYPE_CHECKING, Any
import json
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool, Tool
from pandas.core.frame import DataFrame

if TYPE_CHECKING:
    import pandasql as psql

base_description = "Execute SQL queries on pandas dataframes"


class DataFrameInputField:
    """Field for the SQLQueryInput."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> DataFrame:
        if not isinstance(v, DataFrame):
            raise ValueError('Must be a pandas DataFrame')
        if v.empty:
            raise ValueError('DataFrame must not be empty')
        return v


class SQLQueryInput(BaseModel):
    """Arguments for the SQLQueryTool."""

    sql_query: str = Field(
        ...,
        description=(
            "SQL query to execute on the DataFrame. "
            "Use `dataframe` as Table Name in the SQL query. "
            "It should not be in markdown format."
        ),
        examples=[
            "SELECT * FROM dataframe WHERE column > 10",
            "SELECT AVG(column1) as average_column1 FROM dataframe",
        ],
    )
    max_rows: Optional[int] = Field(
        15,
        description="Maximum number of rows to include in the result"
    )


class PandasSQLQueryTool(BaseTool):
    """Tool that runs SQL queries on a Pandas DataFrame."""

    name: str = "sql_query"
    args_schema: type[BaseModel] = SQLQueryInput
    description: str = base_description
    dataframe: Any

    def __init__(self, dataframe: DataFrameInputField, **kwargs: Any):
        try:
            import pandasql
        except ImportError as e:
            raise ImportError(
                "Unable to import pandasql, please install with `pip install pandasql`."
            ) from e

        super().__init__(description=base_description, **kwargs)
        self.dataframe = dataframe

    def _run(
            self,
            sql_query: str,
            max_rows: Optional[int] = 15,  # Added max_rows parameter
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            globals_dict = {'dataframe': self.dataframe}
            result_df = psql.sqldf(sql_query, globals_dict)
            if max_rows is not None:
                result_df = result_df.head(max_rows)

            result_json = result_df.to_json(orient='records')
            return result_json
        except Exception as e:
            print("Error: " + str(e))
            return json.dumps({"error": str(e)})

    async def _arun(
            self,
            dataframe: DataFrameInputField,
            query: str,
            max_rows: Optional[int] = 15,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> DataFrameInputField:
        raise NotImplementedError(f"{self.name} does not support async")

    def as_tool(self) -> Tool:
        return Tool.from_function(
            func=self._run,
            name=self.name,
            description=self.description,
            args_schema=self.args_schema,
        )
