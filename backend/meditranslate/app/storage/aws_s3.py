import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError

from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.app.loggers import logger
from meditranslate.app.configurations import AWSConfig

class AWSStorageService(BaseStorageService):
    def __init__(self, bucket_name:str,config:AWSConfig):
        self.bucket_name = bucket_name
        self.config = config
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key,
            region_name=self.config.region_name,
            endpoint_url=self.config.endpoint_url,
            config=Config(signature_version='s3v4')
        )

    def upload_file(self, file_obj, filename):
        """
        Upload a file to S3 or LocalStack.
        """
        self.s3_client.upload_fileobj(file_obj, self.bucket_name, filename)


    def download_file(self, file_id):
        """
        Downloads a file from GridFS.

        :param file_id: The ID of the file to download
        :return: The binary content of the file
        """
        try:
            file = self.fs.get(ObjectId(file_id))
            return file.read()
        except gridfs.errors.NoFile:
            logger("File not found.")
            return None

    def delete_file(self, file_id):
        """
        Deletes a file from GridFS.

        :param file_id: The ID of the file to delete
        """
        try:
            self.fs.delete(ObjectId(file_id))
            logger(f"File with ID {file_id} has been deleted.")
        except gridfs.errors.NoFile:
            logger("File not found, nothing to delete.")

    def get_file_metadata(self, file_id):
        """
        Retrieves metadata of a file in GridFS.

        :param file_id: The ID of the file
        :return: Metadata dictionary for the file, or None if not found
        """
        try:
            file = self.fs.get(ObjectId(file_id))
            metadata = {
                "filename": file.filename,
                "upload_date": file.upload_date,
                "size": file.length,
                "content_type": file.content_type if hasattr(file, "content_type") else "unknown"
            }
            return metadata
        except gridfs.errors.NoFile:
            logger("File not found.")
            return None

    def __del__(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()

    def upload_file(self, file_obj, filename):
        """
        Upload a file to S3 or LocalStack, with error handling.
        """
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, filename)
            # Confirm the upload by attempting to get the file's metadata
            self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
            return {"success": True, "message": f"File '{filename}' uploaded successfully."}
        except ClientError as e:
            return {"success": False, "message": f"Failed to upload file: {e.response['Error']['Message']}"}
        except (NoCredentialsError, EndpointConnectionError) as e:
            return {"success": False, "message": f"Configuration error: {str(e)}"}

    def download_file(self, filename):
        """
        Download a file as a stream from S3 or LocalStack, with error handling.
        """
        try:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=filename)
            return {"success": True, "file_stream": s3_object["Body"]}
        except self.s3_client.exceptions.NoSuchKey:
            return {"success": False, "message": "File not found"}
        except ClientError as e:
            return {"success": False, "message": f"Failed to download file: {e.response['Error']['Message']}"}

    def delete_file(self, filename):
        """
        Delete a file from S3 or LocalStack, with error handling.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            # Confirm the deletion by checking if the object still exists
            try:
                self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
                return {"success": False, "message": f"Failed to delete file '{filename}'."}
            except self.s3_client.exceptions.NoSuchKey:
                return {"success": True, "message": f"File '{filename}' deleted successfully."}
        except ClientError as e:
            return {"success": False, "message": f"Failed to delete file: {e.response['Error']['Message']}"}

    def get_file_metadata(self, filename):
        """
        Get metadata of a file in S3 or LocalStack, with error handling.
        """
        try:
            metadata = self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
            return {"success": True, "metadata": metadata["Metadata"], "size": metadata["ContentLength"]}
        except self.s3_client.exceptions.NoSuchKey:
            return {"success": False, "message": "File not found"}
        except ClientError as e:
            return {"success": False, "message": f"Failed to retrieve metadata: {e.response['Error']['Message']}"}


# @Author: mdrhri-6
# @Date:   2016-11-14T18:29:46+01:00
# @Last modified by:   mdrhri-6
# @Last modified time: 2016-11-14T19:44:10+01:00



import boto3
import botocore
import random
import string
import datetime
import matplotlib.pyplot as plt
import numpy as np


class S3Manager:

    # Constructor
    def __init__(self):
        # Create a boto3 resource of type S3
        self.s3 = boto3.resource('s3')
        # Create a client
        self.client = boto3.client('s3')

    '''
        List all the buckets of your region of choice

        Input:
            regions (String) -- [REQUIRED]

        Output:
            list: All the bucket names of the specified regions
    '''

    def list_buckets(self, region):
        bucketList = list()
        for idx, each in enumerate(self.s3.buckets.all()):
            bucketList.insert(idx, each._name)
        return bucketList

    '''
        Create buckets with random name for the given regions list with ACL private.

        Input:
            bucket_name (String) -- Name of the bucket. If none, create a name with a random string
            regions(list) -- [REQUIRED]
            repeat (Integer) -- Number of times you want to repeat the "regions" list(Default is 1)

        Output:
            None
    '''
    def create_buckets(self, bucket_name=None, regions=[], repeat=1):
        if len(regions) == 0:
            print "No region found, please give at least one region name to create bucket."
            return 0
        else:
            regions *= repeat
            for idx, each in enumerate(regions):
                try:
                    # If bucket name is not given, create a random name
                    bucket_name = bucket_name if bucket_name is not None else "".join([random.choice(string.letters) for i in xrange(15)]).lower()
                    kw_args = {
                        'Bucket': bucket_name,
                        'ACL': 'private',
                        'CreateBucketConfiguration': {
                            'LocationConstraint': each
                        }
                    }

                    # Create a bucket
                    bucket = self.client.create_bucket(**kw_args)
                    # Check if the bucket is created successfully of not.
                    if bucket['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print "Created new bucket {} at region {}".format(bucket_name, each)
                    else:
                        print "Can not create a new bucket of name {}".format(bucket_name)

                # Got exception during process.
                except botocore.exceptions.ClientError as e:
                    print "{}".format(e)


    '''
        Upload a file in S3 bucket.

        Input:
            filename (String) -- [REQUIRED]
            bucket (String) -- [REQUIRED]
            key (String) -- [REQUIRED]

        Output:
            Key: The return value. Key for success, False otherwise.
    '''
    def upload_file(self, filename, bucket, key):
        try:
            print "Uploading a new file with key: {}".format(key)
            self.s3.meta.client.upload_file(filename, bucket, key)
            print "Successfully uploaded a file"
            return key

        # Got exception during process.
        except botocore.exceptions.ClientError as e:
            print "Upload failed. Please try again!"
            print e
            return 0



    '''
        Delete a file in S3 bucket.

        Input:
            filename (String) -- [REQUIRED]
            bucket (String) -- [REQUIRED]
            key (String) -- [REQUIRED]

        Output:
            Boolean: The return value. True for success, False otherwise.
    '''
    def delete_file(self, bucket, key):
        try:
            print "Deleting {} from bucket {}".format(key, bucket)
            if bool(self.client.delete_object(Bucket=bucket, Key=key)):
                print "Successfully deleted a file"
                return 1
            else:
                print "You don't have a file with the key: {}. Please try again with a right key".format(key)
                return 0

        # Got exception during process.
        except botocore.exceptions.ClientError as e:
            print "Deletion failed. Please try again!"
            print e
            return 0

    '''
        Download a file from S3 bucket.

        Input:
            bucket (String) -- [REQUIRED]
            key (String) -- [REQUIRED]
            filename (String) -- [REQUIRED]

        Output:
            Boolean: The return value. True for success, False otherwise.
    '''
    def download_file(self, bucket, key, filename):
        try:
            print "Downloading file {} from bucket {}".format(key, bucket)
            self.s3.Bucket(bucket).download_file(key, filename)
            print "Successfully downloded file {}".format(filename)
            return 1
        except botocore.exceptions.ClientError as e:
            print "Download failed. Please try again!"
            print e
            return 0


    '''
        Test object upload & download latency for different regions and plot them in graph.

        *** Hardcoded Method ***
    '''
    def test_latency(self):
        regions = list()
        buckets = list()
        plot_data = list()

        upload_info = list()
        download_info = list()

        files = ['test_1_9MB.pdf', 'test_3MB.pdf', 'test_4_5MB.pdf']
        sizes = [1.9, 3.0, 4.5]

        # Get all the buckets of name 'rafiul' and their location.
        for idx, bucket in enumerate(self.s3.buckets.all()):
            if "rafiul" in bucket.name:
                regions.insert(idx, self.client.get_bucket_location(Bucket=bucket.name)['LocationConstraint'])
                buckets.insert(idx, bucket.name)

        uploaded_data = [[0 for _ in range(len(buckets))] for _ in range(len(regions))]
        downloaded_data = [[0 for _ in range(len(buckets))] for _ in range(len(regions))]

        # Calculate the latency of file upload and download
        for i in range(len(files)):
            for idx, each in enumerate(buckets):
                try:
                    # Upload the file
                    upload_start = datetime.datetime.now().time().strftime('%H:%M:%S')
                    self.upload_file(files[i], each, files[i])
                    upload_end = datetime.datetime.now().time().strftime('%H:%M:%S')

                    # Upload Latency Calculation
                    upload_latency = (datetime.datetime.strptime(upload_end, '%H:%M:%S') - datetime.datetime.strptime(upload_start, '%H:%M:%S'))
                    upload_info.insert((i + idx), (regions[idx], sizes[i], str(upload_latency)))
                    print "\n\n"

                    # Create a new name for the download file.
                    prefix = files[i].split('.')[0]
                    suffix = files[i].split('.')[1]
                    new_file = prefix + str(idx) + '.' + suffix

                    # Download the file with the new name
                    download_start = datetime.datetime.now().time().strftime('%H:%M:%S')
                    self.download_file(each, files[i], new_file)
                    download_end = datetime.datetime.now().time().strftime('%H:%M:%S')

                    # Latency calculation
                    download_latency = (datetime.datetime.strptime(download_end, '%H:%M:%S') - datetime.datetime.strptime(download_start, '%H:%M:%S'))
                    download_info.insert((i + idx), (regions[idx], sizes[i], str(download_latency)))

                    delete = self.delete_file(each, files[i])
                    print "\n\n"
                except botocore.exceptions.ClientError as e:
                    print e

        for each in upload_info:
            for idx, size in enumerate(sizes):
                # import pdb; pdb.set_trace()
                if float(each[1]) == size:
                    num = each[2].split(':')[2]
                    uploaded_data[idx][regions.index((each[0]))] = float(num)

        for each in download_info:
            for idx, size in enumerate(sizes):
                # import pdb; pdb.set_trace()
                if float(each[1]) == size:
                    num = each[2].split(':')[2]
                    downloaded_data[idx][regions.index((each[0]))] = float(num)

        plot_data.insert(0, sizes)
        plot_data.insert(1, uploaded_data)

        plot_data.insert(2, sizes)
        plot_data.insert(3, downloaded_data)

        plot_obj = self.plot_graph(plot_data, regions)
        plot_obj.show()


    '''
        Plot two graphs from data

        Input:
            plot_data (list) -- [REQUIERD] // Can be a list of list or a ndarray(from numpy)
            markers (list): If you want to add identifier inside the graph

        Output:
            plt (Object): PyPlot Object
    '''
    def plot_graph(self, plot_data, markers=[]):
        colors = ['r', 'g', 'b']
        # fig = plt.figure()
        # fig.suptitle('S3 Latency Test', fontsize=14, fontweight='bold')

        f, (ax, ax1) = plt.subplots(2, sharex=True, sharey=True)
        f.suptitle('S3 Upload/Download Latency Test', fontsize=14, fontweight='bold')

        # Upload Graph
        f.subplots_adjust(top=0.90)
        ax.title.set_text("Upload")

        ax.set_xlabel('File Size(MB)')
        ax.set_ylabel('Time(Second)')

        if len(markers) > 0:
            x_high = 0.5
            y_high = 17
            for idx, each in enumerate(plot_data[1]):
                text = str(markers[idx]).upper() + " " + str(each)
                ax.text(x_high, y_high, text, fontsize=12, fontweight='bold', color=colors[idx])
                y_high -= 2

        for idx, each in enumerate(plot_data[1]):
            ax.plot(plot_data[0], each, marker='o', color=colors[idx])
        ax.axis([0, 5, 0, 20])

        # Download Graph
        f.subplots_adjust(top=0.90)
        ax1.title.set_text("Download")

        ax1.set_xlabel('File Size(MB)')
        ax1.set_ylabel('Time(Second)')

        if len(markers) > 0:
            x_high = 0.5
            y_high = 17
            for idx, each in enumerate(plot_data[3]):
                text = str(markers[idx]).upper() + " " + str(each)
                ax1.text(x_high, y_high, text, fontsize=12, fontweight='bold', color=colors[idx])
                y_high -= 2

        for idx, each in enumerate(plot_data[3]):
            ax1.plot(plot_data[2], each, marker='o', color=colors[idx])
        ax1.axis([0, 5, 0, 20])
        return plt
