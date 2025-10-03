import os
import json
import boto3
from botocore.exceptions import ClientError

def get_secret_dict(secret_name: str, region_name: str = None) -> dict:
    """Отримує секрет із AWS Secrets Manager та повертає як словник"""
    region_name = region_name or os.environ.get("AWS_REGION", "eu-north-1")
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        resp = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise RuntimeError(f"Unable to retrieve secret: {e}")

    secret_string = resp.get("SecretString")
    if secret_string:
        return json.loads(secret_string)

    import base64
    return json.loads(base64.b64decode(resp["SecretBinary"]))

def build_sqlalchemy_url_from_secret(secret: dict) -> str:
    """Будує SQLAlchemy URL з словника секрету"""
    user = secret.get("username") or secret.get("MYSQL_USER") or secret.get("user")
    pwd = secret.get("password") or secret.get("MYSQL_PASSWORD") or secret.get("pass")
    host = secret.get("host") or secret.get("MYSQL_HOST")
    db = secret.get("database") or secret.get("MYSQL_DATABASE") or secret.get("db")
    port = secret.get("port", 3306)

    if not all([user, pwd, host, db]):
        raise ValueError("Secret JSON must include username, password, host and database")

    return f"mysql://{user}:{pwd}@{host}:{port}/{db}"
