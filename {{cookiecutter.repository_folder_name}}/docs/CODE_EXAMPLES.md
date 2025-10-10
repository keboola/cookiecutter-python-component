### Defining datatypes

For column data types always use BaseType definitions:
  ```python
# Base Type column examples  
integer_col = ColumnDefinition(BaseType.integer(default=0))  
timestamp_col = ColumnDefinition(BaseType.timestamp())  
date_col = ColumnDefinition(BaseType.date())  
numeric_col = ColumnDefinition(BaseType.numeric(length="38,2"))  
string_col = ColumnDefinition(BaseType.string())  
float_col = ColumnDefinition(BaseType.float())
```


### Loading configuration parameters:

```python
from keboola.component import CommonInterface
# Logger is automatically set up based on the component setup (GELF or STDOUT)
import logging

SOME_PARAMETER = 'some_user_parameter'
REQUIRED_PARAMETERS = [SOME_PARAMETER]

# init the interface
# A ValueError error is raised if the KBC_DATADIR does not exist or contains non-existent path.
ci = CommonInterface()

# A ValueError error is raised if the config.json file does not exists in the data dir.
# Checks for required parameters and throws ValueError if any is missing.
ci.validate_configuration_parameters(REQUIRED_PARAMETERS)

# print KBC Project ID from the environment variable if present:
logging.info(ci.environment_variables.project_id)

# load particular configuration parameter
logging.info(ci.configuration.parameters[SOME_PARAMETER])
```
### Creating a table with predefined schema
```python
from keboola.component import CommonInterface  
from keboola.component.dao import ColumnDefinition, BaseType  
import csv  
  
# init the interface  
ci = CommonInterface()  

# get user parameters  
parameters = ci.configuration.parameters  
  
api_token = parameters['#api_token']
  
# Define complete schema upfront (note that it is also possible to define the schema later, it just has to be defined before the manifest is written)  
schema = {  
    "id": ColumnDefinition(  
        data_types=BaseType.integer(),  
        primary_key=True # This column is the primary key, multiple columns can be defined as primary keys  
    ),  
    "created_at": ColumnDefinition(  
        data_types=BaseType.timestamp()  
    ),  
    "status": ColumnDefinition(), # Default type is string  
    "value": ColumnDefinition(  
        data_types=BaseType.numeric(length="38,2")  
    )  
}  
  
# Create table definition with predefined schema  
out_table = ci.create_out_table_definition(  
    name="results.csv",  # File name for the output  
    destination="out.c-data.results",  # Destination table in Keboola Storage  
    schema=schema,  # Predefined schema (you can omit this if you want to define the schema later)  
    incremental=True,  # Enable incremental loading (primary key must be defined in schema)  
    has_header=True,  # Indicates that the CSV has a header row (True by default, can be defined later)  
)  
  
# Write some data to the output file  
with open(out_table.full_path, 'w+', newline='') as _f:  
    writer = csv.DictWriter(_f, fieldnames=out_table.column_names)  
    writer.writeheader()  
    writer.writerow({  
        "id": "1",  
        "created_at": "2023-01-15T14:30:00Z",  
        "status": "completed",  
        "value": "123.45"  
    })  
  
# Write manifest file so that Keboola knows about the output table schema  
ci.write_manifest(out_table)
```

### Writing a table with dynamic schema

It may happen that it is not known upfront what is the schema of the result data. In this case, you can use `keboola.csvwriter`package that can dynamically adjust the schema as the data comes. The schema of the existing output table in Keboola must always be a subset of what you're trying to write, so you need to store the existing table schema in the state.

```python
from keboola.component import CommonInterface  
from keboola.csvwriter import ElasticDictWriter  
  
# init the interface  
ci = CommonInterface()  
# data with different headers  
data = [{  
    "id": "1",  
    "created_at": "2023-01-15T14:30:00Z",  
    "value": "123.45"  
},  
    {  
        "id": "2",  
        "created_at": "2023-01-15T14:30:00Z",  
        "new_value": "completed",  
        "value": "123.45"  
    }  
]  
  
# Create table definition with predefined schema  
out_table = ci.create_out_table_definition(  
    name="results_dynamic.csv",  # File name for the output  
    destination="out.c-data.results",  # Destination table in Keboola Storage  
    incremental=True,  # Enable incremental loading (primary key must be defined in schema)  
    has_header=True,  # Indicates that the CSV has a header row (True by default, can be defined later)  
)  
  
# get previous columns from state file  
last_state = ci.get_state_file() or {}  
columns = last_state.get("table_column_names", {}).get(out_table.destination, [])  
  
writer = ElasticDictWriter(out_table.full_path,  
                           fieldnames=columns  # initial column name set  
                           )  
# Write some data to the output file  
writer.writerows(data)  
  
writer.writeheader() # this is important as it includes the header in the data, otherwise the first row is treated as data
  
writer.close()  
final_column_names = writer.fieldnames  # collect final column names from the writer after it's closed  
  
  
# Update the output table definition with the final column names  
out_table.schema = final_column_names  # all columns will be string  
out_table.primary_key = ["id"]  # we know that the id from the provided columns is a primary key  
  
# Update the state file with the final column names  
state_file = {  
    "table_column_names": {  
        out_table.destination: final_column_names  
    }  
}  
# Write manifest file so that Keboola knows about the output table schema  
ci.write_manifest(out_table)  
# Write the state file  
ci.write_state_file(state_file)
```



### Processing state files

[State files](https://developers.keboola.com/extend/common-interface/config-file/#state-file) allow your component to store and retrieve information between runs. This is especially useful for incremental processing or tracking the last processed data.

```python
from keboola.component import CommonInterface
from datetime import datetime
import json

# Initialize the interface
ci = CommonInterface()

# Load state from previous run
state = ci.get_state_file()

# Get the last processed timestamp (or use default if this is the first run)
last_updated = state.get("last_updated", "1970-01-01T00:00:00Z")
print(f"Last processed data up to: {last_updated}")

# Process data (only data newer than last_updated)
# In a real component, this would involve your business logic
processed_items = [
    {"id": 1, "timestamp": "2023-05-15T10:30:00Z"},
    {"id": 2, "timestamp": "2023-05-16T14:45:00Z"}
]

# Get the latest timestamp for the next run
if processed_items:
    # Sort items by timestamp to find the latest one
    processed_items.sort(key=lambda x: x["timestamp"])
    new_last_updated = processed_items[-1]["timestamp"]
else:
    # No new items, keep the previous timestamp
    new_last_updated = last_updated

# Store the new state for the next run
ci.write_state_file({
    "last_updated": new_last_updated,
    "processed_count": len(processed_items),
    "last_run": datetime.now().isoformat()
})

print(f"State updated, next run will process data from: {new_last_updated}")
```

State files can contain any serializable JSON structure, so you can store complex information:

```python
# More complex state example
state = {
    "last_run": datetime.now().isoformat(),
    "api_pagination": {
        "next_page_token": "abc123xyz",
        "chunk_size": 100,
        "total_pages_retrieved": 5
    },
    "processed_ids": [1001, 1002, 1003, 1004],
    "statistics": {
        "success_count": 1000,
        "error_count": 5,
        "skipped_count": 10
    }
}

ci.write_state_file(state)
```

### Handling Errors

```
try:  
    # my code  
    do_something()  
except (UserException) as exc:  
    logging.exception(exc,  
                      extra={"additional_detail": "xxx"}  # additional detail)  
    exit(1)  # 1 is user exception  
    except Exception as exc:  
    logging.exception(exc,  
                      extra={"additional_detail": "xxx"}  # additional detail)  
    exit(2)  # 2 is an unhandled application error
```
### Logging

Always use `logging` library as it's using our rich logger after CommonInterface initialisation.

```python
from keboola.component import CommonInterface
from datetime import datetime
import logging

# init the interface
ci = CommonInterface()

logging.info("Info message")
logging.warning("Warning message")
logging.exception(exception, extra={"additional_detail": "xxx"}) # log errors
```

### ComponentBase

[Base class](https://keboola.github.io/python-component/base.html)
for general Python components. Base your components on this class for simpler debugging.

It performs following tasks by default:

- Initializes the CommonInterface.
- For easier debugging the data folder is picked up by default from `../data` path, relative to working directory when
  the `KBC_DATADIR` env variable is not specified.
- If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
- Executes sync actions -> `run` by default. See the sync actions section.

**Constructor arguments**:

- data_path_override: optional path to data folder that overrides the default behaviour
  (`KBC_DATADIR` environment variable). May be also specified by `-d` or `--data` commandline argument

Raises: `UserException` - on config validation errors.

**Example usage**:

```python
import csv
import logging
from datetime import datetime

from keboola.component.base import ComponentBase, sync_action
from keboola.component import UserException

# configuration variables
KEY_PRINT_HELLO = 'print_hello'

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [KEY_PRINT_HELLO]
REQUIRED_IMAGE_PARS = []


class Component(ComponentBase):

    def run(self):
        '''
        Main execution code
        '''

        # ####### EXAMPLE TO REMOVE
        # check for missing configuration parameters
        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        self.validate_image_parameters(REQUIRED_IMAGE_PARS)

        params = self.configuration.parameters
        # Access parameters in data/config.json
        if params.get(KEY_PRINT_HELLO):
            logging.info("Hello World")

        # get last state data/in/state.json from previous run
        previous_state = self.get_state_file()
        logging.info(previous_state.get('some_state_parameter'))

        # Create output table (Tabledefinition - just metadata)
        table = self.create_out_table_definition('output.csv', incremental=True, primary_key=['timestamp'])

        # get file path of the table (data/out/tables/Features.csv)
        out_table_path = table.full_path
        logging.info(out_table_path)

        # DO whatever and save into out_table_path
        with open(table.full_path, mode='wt', encoding='utf-8', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=['timestamp'])
            writer.writeheader()
            writer.writerow({"timestamp": datetime.now().isoformat()})

        # Save table manifest (output.csv.manifest) from the tabledefinition
        self.write_manifest(table)

        # Write new state - will be available next run
        self.write_state_file({"some_state_parameter": "value"})

        # ####### EXAMPLE TO REMOVE END

    # sync action that is executed when configuration.json "action":"testConnection" parameter is present.
    @sync_action('testConnection')
    def test_connection(self):
        connection = self.configuration.parameters.get('test_connection')
        if connection == "fail":
            raise UserException("failed")
        elif connection == "succeed":
            # this is ignored when run as sync action.
            logging.info("succeed")


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action paramter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
```

#### Sync Actions

[Sync actions](https://developers.keboola.com/extend/common-interface/actions/) provide a way to execute quick, synchronous tasks within a component. Unlike the default `run` action (which executes asynchronously as a background job), sync actions execute immediately and return results directly to the UI.

Common use cases for sync actions:
- Testing connections to external services
- Fetching dynamic dropdown options for UI configuration
- Validating user input
- Listing available resources (tables, schemas, etc.)

### Creating Sync Actions

To create a sync action, add a method to your component class and decorate it with `@sync_action('action_name')`. The framework handles all the details of proper response formatting and error handling.

```python
from keboola.component.base import ComponentBase, sync_action
from keboola.component import UserException

class Component(ComponentBase):
    def run(self):
        # Main component logic
        pass
        
    @sync_action('testConnection')
    def test_connection(self):
        """
        Tests database connection credentials
        """
        params = self.configuration.parameters
        connection = params.get('connection', {})
        
        # Validate connection parameters
        if not connection.get('host') or not connection.get('username'):
            raise UserException("Connection failed: Missing host or username")
            
        # If no exception is raised, the connection test is considered successful
        # The framework automatically returns {"status": "success"}
```

## Returning Data from Sync Actions

Sync actions can return data that is used by the UI, such as dropdown options:

```python
from keboola.component.base import ComponentBase, sync_action
from keboola.component.sync_actions import SelectElement

class Component(ComponentBase):
    @sync_action('listTables')
    def list_tables(self):
        """
        Returns list of available tables for configuration dropdown
        """
        # In a real scenario, you would fetch this from a database or API
        available_tables = [
            {"id": "customers", "name": "Customer Data"},
            {"id": "orders", "name": "Order History"},
            {"id": "products", "name": "Product Catalog"}
        ]
        
        # Return as list of SelectElement objects for UI dropdown
        return [
            SelectElement(value=table["id"], label=table["name"])
            for table in available_tables
        ]
```

### Validation Message Action

You can provide validation feedback to the UI:

```python
from keboola.component.base import ComponentBase, sync_action
from keboola.component.sync_actions import ValidationResult, MessageType

class Component(ComponentBase):
    @sync_action('validateConfiguration')
    def validate_config(self):
        """
        Validates the component configuration
        """
        params = self.configuration.parameters
        
        # Check configuration parameters
        if params.get('extraction_type') == 'incremental' and not params.get('incremental_key'):
            # Return warning message that will be displayed in UI
            return ValidationResult(
                "Incremental extraction requires specifying an incremental key column.",
                MessageType.WARNING
            )
            
        # Check for potential issues
        if params.get('row_limit') and int(params.get('row_limit')) > 1000000:
            # Return info message
            return ValidationResult(
                "Large row limit may cause performance issues.",
                MessageType.INFO
            )
            
        # Success with no message
        return None
```

##### No output

Some actions like test connection button expect only success / failure type of result with no return value.

```python
from keboola.component.base import ComponentBase, sync_action
from keboola.component import UserException
import logging


class Component(ComponentBase):

    def __init__(self):
        super().__init__()

    @sync_action('testConnection')
    def test_connection(self):
        # this is ignored when run as sync action.
        logging.info("Testing Connection")
        print("test print")
        params = self.configuration.parameters
        connection = params.get('test_connection')
        if connection == "fail":
            raise UserException("failed")
        elif connection == "succeed":
            # this is ignored when run as sync action.
            logging.info("succeed")
```