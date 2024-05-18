import json

import boto3
import pytest
from moto import mock_aws
from boto3 import client
import utils.downloadJson as downloadJson
REGION = "us-west-2"

@pytest.fixture(scope="function", autouse=True)
def mock_session() -> boto3.Session:
    #with mock_aws():
    #    s3_client = client("s3")
    #    yield s3_client
    with mock_aws():
        session = boto3.Session(
            aws_access_key_id="FAKEKEY",
            aws_secret_access_key="FAKESECRET",
            region_name="REGION"
        )
        bucket_name = "meu-bucket"
        config = {"LocationConstraint": REGION}
        s3_client = session.client("s3")
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=config)
        object_key = "meu-objeto.json"
        j = [{"nome": "endereco", "campos": [
            {"Field": "id", "Type": "int", "Null": "NO", "Key": "PRI", "Default": "None", "Extra": "auto_increment"},
            {"Field": "rua", "Type": "varchar(200)", "Null": "YES", "Key": "", "Default": "None", "Extra": ""},
            {"Field": "numero", "Type": "varchar(200)", "Null": "YES", "Key": "", "Default": "None", "Extra": ""}]}]
        object_body = json.dumps(j)

        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=object_body)
        yield session




def test_create_bucket(mock_session: boto3.Session):
    bucket_name = "meu-bucket"

    bucket = mock_session.list_buckets()["Buckets"][0]
    assert bucket["Name"] == bucket_name


def test_get_json_of_bucket(mock_session: boto3.Session):
    bucket_name = "meu-bucket"
    object_key = "meu-objeto.json"

    response = downloadJson.getJsonBucket(mock_session,nameBucket=bucket_name, nameFile=object_key)
    assert response == response
