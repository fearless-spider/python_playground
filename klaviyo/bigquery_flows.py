from google.cloud import bigquery

from google.oauth2 import service_account
from dotenv import load_dotenv
load_dotenv()

client = bigquery.Client()
filename = 'flows.json'
dataset_id = 'klaviyo_2024'
table_id = 'flows'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
job_config.autodetect = True

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location="US",  # Must match the destination dataset location.
        job_config=job_config,
    )  # API request

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
