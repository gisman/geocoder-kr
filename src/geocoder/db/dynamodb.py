# import leveldb
import boto3
import json
from geocoder.db.base import DbBase


class DynamoDbGeocode(DbBase):
    """
    A class to interact with DynamoDB for geocoding operations.
    """

    def __init__(self, db_name, **kwargs):
        """
        Initialize the DynamoDbGeocode instance.

        :param db_name: The name of the DynamoDB resource.
        :param kwargs: Additional keyword arguments for boto3 resource and client.
        """
        self.db = boto3.resource(db_name, **kwargs)
        self.dynamodb_client = boto3.client("dynamodb", **kwargs)
        self.table_name = "geocode"
        self.table = self.db.Table(self.table_name)

    def init_table(self, table_name):
        """
        Initialize the DynamoDB table.

        :param table_name: The name of the table to initialize.
        :return: The initialized table.
        """
        self.table_name = table_name
        try:
            table = self.db.Table(table_name)
            if table.table_status:
                self.table = table
                return table
        except self.dynamodb_client.exceptions.ResourceNotFoundException:
            table = self.db.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "key", "KeyType": "HASH"}  # Partition key
                ],
                AttributeDefinitions=[{"AttributeName": "key", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            self.table = table
            return table
            # return self

    def get(self, k):
        """
        Retrieve an item from the DynamoDB table.

        :param k: The key of the item to retrieve.
        :return: The value of the retrieved item.
        """
        response = self.table.get_item(Key={"key": k})
        return response["Item"]["val"]

    def delete(self, k):
        """
        Delete an item from the DynamoDB table.

        :param k: The key of the item to delete.
        """
        self.dynamodb_client.delete_item(self.table_name, Item={"key": k})

    def put(self, k, v):
        """
        Put an item into the DynamoDB table.

        :param k: The key of the item to put.
        :param v: The value of the item to put.
        """
        self.dynamodb_client.put_item(
            TableName=self.table_name, Item={"key": {"S": k}, "val": {"S": v}}
        )

    def BatchPut(self, keys, vals):
        """
        Batch put multiple items into the DynamoDB table.

        :param keys: A list of keys for the items.
        :param vals: A list of values for the items.
        """
        batch = {"geocode": []}
        for i in range(len(keys)):
            batch["geocode"].append(
                {"PutRequest": {"Item": {"key": {"S": keys[i]}, "val": {"S": vals[i]}}}}
            )

        self.dynamodb_client.batch_write_item(RequestItems=batch)
