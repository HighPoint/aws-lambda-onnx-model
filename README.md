# aws-lambda-onnx-model

Run LARGE machine learning models on AWS Lambda with ONNX. The ONNX models can be over 1 GBs.

![ONNX](https://user-images.githubusercontent.com/5720767/154100057-06d25a00-cfd5-40a6-b4c4-a303bbcaf5d7.jpg)



This model has two dependencies, the python Pillow and onnxruntime libraries. These need to be added as AWS Lambda Layers. Numpy is included in the onnxruntime. 

In order to create the Lambda Layers, do a Docker pull:


    docker pull highpoints/aws-lambda-layer-zip-builder:latest  



Then run:



    docker run --rm -v $(pwd):/package highpoints/aws-lambda-layer-zip-builder Pillow  
    docker run --rm -v $(pwd):/package highpoints/aws-lambda-layer-zip-builder onnxruntime 


This should create:



    pillow3.8.5.zip  
    onnxruntime3.8.5.zip

Add these as your AWS Lambda Layers. Make sure you include the key "PYTHONPATH" with the value "/opt/" in the AWS Lambda Environmental Variables configuration.



Happy Coding!
