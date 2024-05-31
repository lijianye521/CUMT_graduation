# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
import subprocess
from django.http import StreamingHttpResponse

import torch
from transformers import XLNetTokenizer, XLNetForSequenceClassification
import numpy as np
import pandas as pd
import os
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    file = request.FILES.get('file')
    if file:
        dataset_path = os.path.join(settings.BASE_DIR, 'dataset')
        path = default_storage.save(os.path.join(dataset_path, file.name), ContentFile(file.read()))
        return Response({"message": "文件上传成功", "path": path})
    return Response({"message": "没有检测到文件"}, status=400)

@api_view(['GET'])
def list_datasets(request):
    dataset_path = os.path.join(settings.BASE_DIR, 'dataset')  # 确保 'dataset' 目录在你的项目根目录下
    datasets = [f for f in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, f))]
    return Response(datasets)
@api_view(['GET'])
def list_models(request):
    model_path = os.path.join(settings.BASE_DIR, 'model')  # 确保 'dataset' 目录在你的项目根目录下
    models = [f for f in os.listdir(model_path) if os.path.isfile(os.path.join(model_path, f))]
    return Response(models)
@api_view(['POST'])
def predict(request):
    data = request.data
    print("Received data from frontend:", data)
    
    # 合并 summary 和 description
    combined_text = f"{data.get('summary', '')} {data.get('description', '')} {data.get('component', '')} {data.get('severity', '')} {data.get('priority', '')}"    
    print("Combined Text:", combined_text)
    
    # 定义模型和tokenizer的路径
    MODEL_PATH = str(settings.BASE_DIR / 'model/xlnet_openoffice.pth')
    TOKENIZER_PATH = 'xlnet-base-cased'
    CSV_FILE_PATH = str(settings.BASE_DIR / 'dataset/OpenOffice_total_10_10.csv')

    # 指定需要提取的列
    columns_to_extract = ['developer']
    df = pd.read_csv(CSV_FILE_PATH, usecols=columns_to_extract, encoding='latin-1')

    # 将developer列作为标签
    label_dict = {label: idx for idx, label in enumerate(df['developer'].unique())}
    reverse_label_dict = {v: k for k, v in label_dict.items()}  # 反向字典用于从索引获取开发者名称

    # 加载模型和tokenizer
    tokenizer = XLNetTokenizer.from_pretrained(TOKENIZER_PATH)
    model = XLNetForSequenceClassification.from_pretrained(TOKENIZER_PATH, num_labels=len(label_dict))

    # 加载训练好的模型参数
    checkpoint = torch.load(MODEL_PATH)
    model.load_state_dict(checkpoint['model_state_dict'], strict=False)
    model.eval()

    # 定义设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    def predict_developers(text):
        # 对输入文本进行编码
        inputs = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=512
        )

        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
        
        logits = outputs[0]
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]

        # 获取前10个开发者及其概率
        topk_indices = np.argsort(probabilities)[-10:][::-1]
        topk_probabilities = probabilities[topk_indices]

        results = [(reverse_label_dict[idx], prob) for idx, prob in zip(topk_indices, topk_probabilities)]
        
        return results

    # 获取预测结果
    predicted_developers = predict_developers(combined_text)

    # 构建返回结果列表
    result_list = [f"开发者: {developer}, 可能性: {probability:.4f}" for developer, probability in predicted_developers]
    print(result_list)
    return Response({"message": "Data received successfully", "predictions": result_list}, status=status.HTTP_200_OK)
def hello_world_view(request):
    return HttpResponse('Hello World')

import os

# 在 TrainBERTView 类的 post 方法中，使用 StreamingHttpResponse 返回命令行输出，以便前端能够捕获信息

class TrainBERTView(APIView):
    def post(self, request, *args, **kwargs):
        dataset = request.data.get('dataset')
        model = request.data.get('model')
        checkpoint_path = request.data.get('checkpointPath')
        experiment_num = request.data.get('experimentNum')
        optional_feature = request.data.get('optionalFeature')

        print("接收到的参数:")
        print("数据集:", dataset)
        # print("模型:", model)
        print("检查点路径:", checkpoint_path)
        print("实验编号:", experiment_num)
        print("可选特性:", optional_feature)

        dataset_path = os.path.join(settings.BASE_DIR, 'dataset', dataset)
        model_path = os.path.join(settings.BASE_DIR, 'model', model)

        command = (
            f"python bert.py --dataset {dataset_path} --model {model_path} "
            f"--checkpoint_path {checkpoint_path} "
            f"--experiment_num {experiment_num} "
            f"--optional_feature {optional_feature}"
        )

        # 创建一个生成器，用于执行命令并逐行捕获输出
        def generate():
            process = os.popen(command)
            for line in process:
                yield f"data: {line}\n\n"
        # 创建并返回一个 StreamingHttpResponse 对象，使用生成器作为内容
        response = StreamingHttpResponse(generate(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response
# class TrainBERTView(APIView):
#     def post(self, request, *args, **kwargs):
#         # 提取发送的数据
#         dataset = request.data.get('dataset')
#         model = request.data.get('model')
#         checkpoint_path = request.data.get('checkpointPath')
#         experiment_num = request.data.get('experimentNum')
#         optional_feature = request.data.get('optionalFeature')
#         # 打印接收到的参数
#         print("接收到的参数:")
#         print("数据集:", dataset)
#         print("模型:", model)
#         print("检查点路径:", checkpoint_path)
#         print("实验编号:", experiment_num)
#         print("可选特性:", optional_feature)

#         # 组装命令
#         command = (
#             f"python bert.py --dataset {'./dataset/'+dataset} --model {model} "
#             f"--checkpoint_path {checkpoint_path} "
#             f"--experiment_num {experiment_num}"
#             f"--optional_feature {optional_feature}"
#         )
#         print("执行的命令:", command)
#         # 创建一个生成器，用于执行命令并逐行捕获输出
#         def generate():
#             with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
#                 for line in process.stdout:
#                     yield f"data: {line}\n\n"
#         # 创建并返回一个 StreamingHttpResponse 对象，使用生成器作为内容
#         response = StreamingHttpResponse(generate(), content_type="text/event-stream")
#         response['Cache-Control'] = 'no-cache'
#         return response
