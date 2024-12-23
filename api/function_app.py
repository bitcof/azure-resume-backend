from azure.data.tables import TableClient, UpdateMode
import azure.functions as func
import json
import os


connection_string = os.getenv("CosmosDbConnectionSetting")
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="get_resume_count")
def get_resume_count(req: func.HttpRequest) -> func.HttpResponse:
    count = 30
    with TableClient.from_connection_string(conn_str=connection_string, table_name="AzureResume") as table_client:
        count_entity = table_client.get_entity(partition_key=str(1), row_key=str(1))
        count = count_entity["Count"]
        count_entity["Count"] = count + 1
        table_client.update_entity(mode=UpdateMode.REPLACE, entity=count_entity)

    return func.HttpResponse(
        json.dumps({"count": count}),
        status_code=200,
    )
