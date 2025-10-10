
### API Token & Secret Values

Always prefix private parameters like passwords with `#` character. These will be automatically hashed and hidden from the view. 
Use a textual input field with `"format":"password"` in the JsonSchema for these values to hide the content also during the typing.

```json
{
    "#api_token": {
        "type": "string",
        "title": "API token",
        "format": "password",
        "propertyOrder": 1
    }
}
```


### Checkboxes

```json
{
    "campaigns": {
        "type": "boolean",
        "title": "Download Campaigns",
        "default": false,
        "format": "checkbox",
        "propertyOrder": 30
    },
    "segments": {
        "type": "boolean",
        "title": "Download Segments",
        "default": false,
        "format": "checkbox",
        "propertyOrder": 40
    }
}
```

### Tooltips

Additional description with optional links

```json
{
  "test_tooltip": {
    "type": "string",
    "title": "Example tooltip",
    "options": {
      "tooltip": "custom tooltip, default is Open documentation"
    },
    "description": "Test value.",
    "propertyOrder": 1
  }
}
```



### Multi Selection

```json
{
    "types": {
        "type": "array",
        "title": "Types",
        "description": "Activity types",
        "items": {
            "enum": [
                "page",
                "event",
                "attribute_change",
                "failed_attribute_change",
                "stripe_event",
                "drafted_email",
                "failed_email",
                "dropped_email",
                "sent_email",
                "spammed_email",
                "bounced_email",
                "delivered_email",
                "triggered_email",
                "opened_email"
            ],
            "type": "string"
        },
        "format": "select",
        "uniqueItems": true,
        "propertyOrder": 360
    }
}
```


### Creatable Multi Select

Multi select with user creatable values

```json
{
  "test_creatable_multi_select": {
    "propertyOrder": 50,
    "type": "array",
    "items": {
      "type": "string"
    },
    "format": "select",
    "options": {
      "tags": true
    },
    "description": "Multi-select element with no enum => user creates arbitrary values. Comma-separated values are supported.",
    "uniqueItems": true
  }
}
```

### Codemirror (json/sql/python..) Editor

Allow inject Codemirror editor to a JSON schema based UI. 
Allowed options: mode, placeholder, autofocus, lineNumbers lint
Available modes: `text/x-sfsql`, `text/x-sql`, `text/x-plsql`, `text/x-python`, `text/x-julia`, `text/x-rsrc`, `application/json`
JSON mode supports encryption. Default mode is `application/json` . You should set type base on mode (string or object).

**JsonSchema examples:**

```json
{
  "token": {
    "type": "object",
    "format": "editor"
  }
}
```

```json
{
  "sql": {
    "type": "string",
    "format": "editor",
    "options": {
      "editor": {
        "mode": "text/x-sql"
      }
    }
  }
}
```

```json
{
  "json_properties": {
      "type": "object",
      "title": "User Parameters",
      "format": "editor",
      "default": {
        "debug": false
      },
      "options": {
        "editor": {
          "lint": true,
          "mode": "application/json",
          "lineNumbers": true,
          "input_height": "100px"
        }
      },
      "description": "User parameters accessible, the result will be injected in standard data/config.json parameters property as in any other component",
      "propertyOrder": 1
    }
}
```

### Trimmed String

Works only for simple string inputs. Value is trimmed before save.

**JsonSchema example:**

```json
"token": {
  "type": "string",
  "format": "trim"
}
```



### Date Range

When a date range is applicable, it should be bounded by two parameters: *From Date* and *To Date*. 
These should be the text fields that accept a particular date in a specified format or a string defining a relative 
interval in [strtotime](https://www.php.net/manual/en/function.strtotime.php) manner. 

**Tip:** A convenient Python function for parsing such values and conversion to date can be found in the Keboola python-utils library 
([parse_datetime_interval](https://github.com/keboola/python-utils#getting-converted-date-period-from-string)).

```json
{
    "date_from": {
        "propertyOrder": 5,
        "type": "string",
        "title": "From date [inclusive]",
        "description": "Date from. Date in YYYY-MM-DD format or a string i.e. 5 days ago, 1 month ago, yesterday, etc. If left empty, all records are downloaded."
    },
    "date_to": {
        "propertyOrder": 7,
        "type": "string",
        "title": "To date [exclusive]",
        "default": "now",
        "description": "Date to. Date in YYYY-MM-DD format or a string i.e. 5 days ago, 1 month ago, yesterday, etc. If left empty, all records are downloaded."
    }
}
```


### Loading Options (Incremental vs Full)

This may be combined in [loading options block](/extend/component/ui-options/configuration-schema/examples/#example-1---object-blocks-loading-options).

```json
{
    "incremental_output": {
        "type": "number",
        "enum": [
            0,
            1
        ],
        "options": {
            "enum_titles": [
                "Full Load",
                "Incremental Update"
            ]
        },
        "default": 1,
        "title": "Load type",
        "description": "If set to Incremental update, the result tables will be updated based on the primary key. Full load overwrites the destination table each time. NOTE: If you wish to remove deleted records, this needs to be set to Full load and the Period from attribute empty.",
        "propertyOrder": 365
    }
}
```

### Visual Separation of Sections

It often happens that the configuration can be split into multiple sections. 
It is advisable to split these visually using JSON Schema objects or arrays to achieve it using the generic UI.

#### Example 1 – Object blocks (loading options)

Loading options block:

```json
{
    "loading_options": {
        "type": "object",
        "title": "Loading Options",
        "propertyOrder": 400,
        "format": "grid",
        "required": [
            "incremental_output",
            "date_since",
            "date_to"
        ],
        "properties": {
            "date_since": {
                "type": "string",
                "title": "Period from date [including].",
                "default": "1 week ago",
                "description": " Date in YYYY-MM-DD format or dateparser string, i.e., 5 days ago, 1 month ago, yesterday, etc. If left empty, all records are downloaded.",
                "propertyOrder": 300
            },
            "date_to": {
                "type": "string",
                "title": "Period to date [excluding].",
                "default": "now",
                "description": " Date in YYYY-MM-DD format or dateparser string, i.e., 5 days ago, 1 month ago, yesterday, etc. If left empty, all records are downloaded.",
                "propertyOrder": 400
            },
            "incremental_output": {
                "type": "number",
                "enum": [
                    0,
                    1
                ],
                "options": {
                    "enum_titles": [
                        "Full Load",
                        "Incremental Update"
                    ]
                },
                "default": 1,
                "title": "Load type",
                "description": "If set to Incremental update, the result tables will be updated based on the primary key. Full load overwrites the destination table each time. NOTE: If you wish to remove deleted records, this needs to be set to Full load and the Period from attribute empty.",
                "propertyOrder": 450
            }
        }
    }
}
```

#### Example 2 – Optional blocks using arrays

Create an array with parameter `"maxItems": 1` to create optional blocks.

```json
{
    "customers": {
        "type": "array",
        "title": "Customers",
        "description": "Download Customers.",
        "propertyOrder": 4000,
        "maxItems": 1,
        "items": {
            "type": "object",
            "title": "Setup",
            "required": [
                "filters",
                "attributes"
            ],
            "properties": {
                "filters": {
                    "type": "string",
                    "title": "Filter",
                    "description": "Optional JSON filter, as defined in https://customer.io/docs/api-triggered-data-format#general-syntax. Example value: {\"and\":[{\"segment\":{\"id\":7}},{\"segment\":{\"id\":5}}]} If left empty, all users are downloaded",
                    "format": "textarea",
                    "propertyOrder": 1
                },
                "attributes": {
                    "type": "string",
                    "title": "Attributes",
                    "format": "textarea",
                    "options": {
                        "input_height": "100px"
                    },
                    "description": "Comma-separated list of required customer attributes. Each customer may have different set of columns, this is to limit only to attributes you need. All attributes are downloaded if left empty.",
                    "uniqueItems": true,
                    "propertyOrder": 700
                }
            }
        }
    }
}
```



### Changing Set of Options Dynamically Based on Selection

In some cases, a different set of options is available for different types of the same object, e.g., Report type. 
JSON Schema allows to define different schemas based on selection. 
This may be useful in the configuration rows scenario, where each row could represent a different type of Report, Endpoint, etc.

This can be achieved via [dependencies](https://github.com/json-editor/json-editor#dependencies).* 


```json
{
  "type": "object",
  "title": "extractor configuration",
  "required": [
    "download_attachments"

  ],
  "properties": {
    "download_attachments": {
      "type": "boolean",
      "format": "checkbox",
      "title": "Download Attachments",
      "description": "When set to true, also the attachments will be downloaded. By default into the File Storage. Use processors to control the behaviour.",
      "default": false,
      "propertyOrder": 300
    },
    "attachment_pattern": {
      "type": "string",
      "title": "Attachment Pattern",
      "description": "Regex pattern to filter particular attachments, e.g., to retrieve only pdf file types use: .+\\.pdf If left empty, all attachments are downloaded.",
      "default": ".+\\.csv",
      "options": {
        "dependencies": {
          "download_attachments": true
        }
      },
      "propertyOrder": 400
    }
  }
}
```


You can also react on multiple array values or on multiple elements at the same time.:

```json
"options": {
  "dependencies": {
    "endpoint": [
      "analytics_data_breakdown_by_content", "analytics_data_breakdown_by_object"
    ],
    "filtered": false
  }
}
```

# Json Schema UI elements with Sync Actions
Some UI elements use [sync actions](https://developers.keboola.com/extend/common-interface/actions/) to get some values dynamically 
from the component code. This section provides a list of the elements currently supported. 

Each element specifies the `action` attribute, which relates to the name of the sync action registered in the Developer Portal.

***Note:** Support for these elements is also abstracted in the official [Python Component library](https://github.com/keboola/python-component#framework-support).*

### Dynamically Loaded Dropdowns

Drop-down lists (values and labels) can be loaded by the component sync action. 

The sync action code has to return the following stdout:

```
[
 { label: 'Joe', value: 'joe' },
 { label: 'Doe', value: 'doe },
 { label: 'Jane', value: 'jane' }
]
```

The `label` value is optional. 

When used in Python, you can use the [SelectElement](https://github.com/keboola/python-component#selectelement) class as a return value.

#### Dynamically loaded multi select

```json
{
    "test_columns": {
      "type": "array",
      "propertyOrder": 10,
      "description": "Element loaded by an arbitrary sync action.",
      "items": {
        "enum": [],
        "type": "string"
      },
      "format": "select",
      "options": {
        "async": {
          "label": "Re-load test columns",
          "action": "testColumns"
        }
      },
      "uniqueItems": true
    }
}
```

#### Dynamically loaded single select

```json
{
  "test_columns_single": {
    "propertyOrder": 40,
    "type": "string",
    "description": "Element loaded by an arbitrary sync action (single).",
    "enum": [],
    "format": "select",
    "options": {
      "async": {
        "label": "Re-load test columns",
        "action": "testColumns"
      }
    }
  }
}
```


### Generic Validation Button

This button can be used to return feedback from the component. The output supports Markdown.

Example use cases are query testing, testing connection, report validation, etc.

The sync action code has to return the following stdout (JSON string):

```json
{
  "message": "###This is display text. \n\n It can contain **Markdown** notation. ",
  "type": "info",
  "status": "success"
}
```

**Available options:**
- `type`: possible values: success, info, warning, error, table
- `status`: possible values: success, error

#### Custom Icons

Markdown supports special status icons that are rendered in Keboola UI style. The following icons are supported:

```
![success]()
![warning]()
![error]()
```
When used in Python, you can use the [ValidationResult](https://github.com/keboola/python-component#validationresult) class as a return value.

**NOTE** If status: error is used the message will always be displayed as an error message.

#### Example

```json
{
  "validation_button": {
    "type": "button",
    "format": "sync-action",
    "propertyOrder": 10,
    "options": {
      "async": {
        "label": "Validate",
        "action": "validate_report"
      }
    }
  }
}
```

### Test Connection

This button can be used for simple connection tests. 

The sync action code has to return the following stdout (JSON string) or error (exit code >0):

```json
{
  "status": "success" // this is required and will never be other value than "success"
}
```

The name of this sync action **always has to be `testConnection`.**

When used in Python, the method does not need to return anything, or it can just throw an exception.

#### Example

```json
{
    "test_connection": {
      "type": "button",
      "format": "sync-action",
      "propertyOrder": 30,
      "options": {
        "async": {
          "label": "TEST CONNECTION",
          "action": "validate_connection"
        }
      }
    }
}
```

### Autoload

All sync action types (buttons, select, and multi-selects) can automatically trigger the sync action if not defined on the UI page load. 

#### Example

```json
{
  "endpoint": {
    "type": "string",
    "title": "Endpoint",
    "description": "Use the sync action to get a list of available endpoints.",
    "propertyOrder": 1,
    "options": {
      "async": {
        "label": "List Endpoints",
        "action": "listEndpoints",
        "autoload": []
      }
    },
    "items": {
      "enum": [],
      "type": "string"
    },
    "enum": []
  }
}
```

Additionally, a watch element can be set in an autoload array, which, when defined or changed, will trigger the sync action.

#### Example

```json
{
  "field_names": {
    "type": "array",
    "format": "select",
    "title": "Fields (optional)",
    "description": "List of field names to be downloaded",
    "propertyOrder": 2,
    "options": {
      "async": {
        "label": "List Fields",
        "action": "listFields",
        "autoload": [
          "parameters.endpoint"
        ]
      }
    },
    "items": {
      "enum": [],
      "type": "string"
    },
    "uniqueItems": true
  }
}
```

The autoload option also enables caching loaded values by default, which can be disabled by setting the `autoload.cache` to false.

#### Example

```json
{
  "endpoint": {
    "type": "string",
    "title": "Endpoint",
    "description": "Use a sync action to get a list of available endpoints.",
    "propertyOrder": 1,
    "options": {
      "async": {
        "label": "List Endpoints",
        "action": "listEndpoints",
        "autoload": [],
        "cache": false
      }
    },
    "items": {
      "enum": [],
      "type": "string"
    },
    "enum": []
  }
}
```
