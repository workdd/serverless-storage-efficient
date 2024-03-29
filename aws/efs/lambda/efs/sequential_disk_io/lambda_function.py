from time import time
import subprocess
import os
import boto3
import decimal
import random

tmp = '/tmp/'
mnt_test = '/mnt/efs/'


def lambda_handler(event, context):
    try:
        file_size = int(event['fs'])
        byte_size = int(float(event['bs']) * 1024)

        block = os.urandom(byte_size)
        file_write_path = mnt_test + str(time())
        r_file_size = file_size * 1024 * 1024
        start = time()
        with open(file_write_path, 'wb', 0) as f:
            for idx in range(int(r_file_size / byte_size)):
                f.seek(byte_size * (idx + 1))
                f.write(block)
                f.flush()
                os.fsync(f.fileno())
        disk_write_latency = time() - start
        disk_write_bandwidth = file_size / disk_write_latency

        # output = subprocess.check_output(['ls', '-alh', mnt_test])

        start = time()
        with open(file_write_path, 'rb', 0) as f:
            for _ in range(int(r_file_size / byte_size)):
                f.read(byte_size)
        disk_read_latency = time() - start
        disk_read_bandwidth = file_size / disk_read_latency

        rm = subprocess.Popen(['rm', '-rf', file_write_path])
        rm.communicate()

        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'efs',
                'second_type': 'sequence',
                'disk_write_bandwidth': decimal.Decimal(str(disk_write_bandwidth)),
                'disk_write_latency': decimal.Decimal(disk_write_latency),
                'disk_read_bandwidth': decimal.Decimal(str(disk_read_bandwidth)),
                'disk_read_latency': decimal.Decimal(disk_read_latency),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return {
            'disk_write_bandwidth': disk_write_bandwidth,
            'disk_write_latency': disk_write_latency,
            'disk_read_bandwidth': disk_read_bandwidth,
            'disk_read_latency': disk_read_latency
        }

    except MemoryError as me:
        return event['fs'] + 'MB ' + event['bs'] + 'KB\n'

    except Exception as ex:
        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'efs',
                'second_type': 'sequence',
                'error': str(ex),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return event['fs'] + 'MB ' + event['bs'] + 'KB\n'
