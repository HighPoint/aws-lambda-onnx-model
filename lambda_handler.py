import json
import onnxruntime
from PIL import Image
import numpy as np
import io
import boto3

def lambda_handler(event, context):

    bucket = "YOUR BUCKET NAME"
    key = "YOUR KEY NAME"
    model_key = "super-resolution-10.onnx"
    keyOut = "onnxTestImage.jpg"

    fileStream = openFilefromS3(bucket, key)
    fileBinary = fileStream.getvalue()

    modelStream = openFilefromS3(bucket, model_key)
    modelBinary = modelStream.getvalue()

    original_image = Image.open(io.BytesIO(fileBinary))
    ycbcr_image, img_cb, img_cr = processImageYCbCr(original_image)

    onnx_image = onnxModel(ycbcr_image, modelBinary)
    rgb_image = processImageRGB(onnx_image, img_cb, img_cr)
    output = io.BytesIO()

    rgb_image.save(output, format='JPEG')
    output.seek(0)

    save_S3_from_memory( output, bucket, keyOut)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def onnxModel(image, modelBinary):

    # log warnings

    so = onnxruntime.SessionOptions()
    so.log_severity_level = 3

    # log warnings end

    ort_session = onnxruntime.InferenceSession(modelBinary, sess_options=so)

    ort_inputs = {ort_session.get_inputs()[0].name: image}
    ort_outs = ort_session.run(None, ort_inputs)
    img_out_y = ort_outs[0]

    return img_out_y

def processImageYCbCr(img):

    img_resize = img.resize((224, 224))
    img_ycbcr = img_resize.convert('YCbCr')

    img_y_0, img_cb, img_cr = img_ycbcr.split()
    img_ndarray = np.asarray(img_y_0)

    img_4 = np.expand_dims(np.expand_dims(img_ndarray, axis=0), axis=0)
    img_5 = img_4.astype(np.float32) / 255.0

    return img_5, img_cb, img_cr

def processImageRGB(img, img_cb, img_cr):

    img_out_y = Image.fromarray(np.uint8((img[0] * 255.0).clip(0, 255)[0]), mode='L')

    final_img = Image.merge(
        "YCbCr", [
            img_out_y,
            img_cb.resize(img_out_y.size, Image.BICUBIC),
            img_cr.resize(img_out_y.size, Image.BICUBIC),
        ]).convert("RGB")

    return final_img

def save_S3_from_memory(buf, bucketName, keyName):

    s3 = boto3.resource('s3')

    object = s3.Object(bucketName, keyName)
    response = object.put(Body=buf)

    return True

def openFilefromS3(bucketName, keyName):

    s3 = boto3.client('s3')
    s3_connection = boto3.resource('s3')

    waiterFlg = s3.get_waiter('object_exists')
    waiterFlg.wait(Bucket=bucketName, Key=keyName)

    s3_object = s3_connection.Object(bucketName,keyName)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())

    return stream
