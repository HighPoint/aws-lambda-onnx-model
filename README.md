# aws-lambda-onnx-model

This model has two dependencies, the python pillow and onnxruntime. These need to be added as AWS Lambda Layers. Numpy is included in the onnxruntime. 

In order to create the Lambda Layers, do a Docker pull:

  docker pull highpoints/aws-lambda-layer-zip-builder:latest

Then run:



    opencv-python  
    numpy
    Pillow
    spaCy



