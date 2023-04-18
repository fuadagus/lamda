# handler.py 
import json
import boto3
import os
import rio_cogeo
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

def noncog_to_cog_tiff(input_img, output_img):
    if rio_cogeo.cog_info(input_img).COG:
        print('The input img is already a COG!')
    else:
        print('The input img is not a COG, starting conversion of input img to COG!')
        cog_translate(input_img, output_img, cog_profiles.get("lzw"))
        if rio_cogeo.cog_info(output_img).COG:
            print(f'finished converting input img to COG! The output img is saved to {output_img}')

def handler(event, context):
    print('start')
    os.mkdir('/tmp/output')
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj_name = key.split('/')[-1]
    full_path = f's3://{bucket_name}/{key}'
    
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(key, f'/tmp/{obj_name}')
    print(obj_name)
    
    noncog_to_cog_tiff(f'/tmp/{obj_name}', f'/tmp/output/{obj_name}')
    
    s3 = boto3.client('s3')
    s3.upload_file(f'/tmp/output/{obj_name}', bucket_name+'-output', 'cog_'+key)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'conversion_to_cog_finished')
    }