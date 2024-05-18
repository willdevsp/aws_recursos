import boto3

def getJsonBucket(session: boto3 ,nameBucket,nameFile):
    print("Recebendo dados para consulta")
    s3Client = boto3.client("s3")
    data = s3Client.get_object(Bucket=nameBucket, Key=nameFile)
    jsonData = data["Body"].read().decode('utf-8')
    print("COnsulta realizada com sucesso", jsonData)
    return jsonData
