import boto3

client = boto3.client('athena')

with open('athena_table.ddl') as ddl:
    create = str(ddl.read())
    context = {'Database': 'athenacaue'}
    response = client.start_query_execution(
        QueryString=create,
        QueryExecutionContext=context,
        ResultConfiguration={
            'OutputLocation': 's3://schematablescaue/schema/',
        }
    )
    print(response)
