# aws-lambda-onnx-model

Run LARGE machine learning models on AWS Lambda with ONNX. The ONNX models can be over 500 MBs.

This model has two dependencies, the python pillow and onnxruntime. These need to be added as AWS Lambda Layers. Numpy is included in the onnxruntime. 

In order to create the Lambda Layers, do a Docker pull:


    docker pull highpoints/aws-lambda-layer-zip-builder:latest  



Then run:



    docker run --rm -v $(pwd):/package highpoints/aws-lambda-layer-zip-builder Pillow  
    docker run --rm -v $(pwd):/package highpoints/aws-lambda-layer-zip-builder onnxruntime 




