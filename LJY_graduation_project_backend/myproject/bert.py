import os
import torch
from tqdm.auto import tqdm
import warnings
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
import pandas as pd
import argparse

# 忽略特定的警告
warnings.filterwarnings("ignore", message="Be aware, overflowing tokens are not returned*")

# 设置命令行参数
parser = argparse.ArgumentParser(description="BERT Model Training")
parser.add_argument('--dataset', type=str, default='./dataset/Eclipse_morethan10_processed_again.csv', help='Path to the dataset file')
parser.add_argument('--checkpoint_path', type=str, default='Bert_Eclipse.pth', help='Path to the model checkpoint file')
parser.add_argument('--experiment_num', type=int, default=13, help='Experiment number')
parser.add_argument('--model_name', type=str, default='xlnet', help='Name of the model')
parser.add_argument('--optional_feature', type=str, default='abstract+descrition', help='Optional features used')
args = parser.parse_args()
# 使用命令行参数
new_file_path = args.dataset
checkpoint_path = args.checkpoint_path
experiment_num = args.experiment_num
model_name = args.model_name
optional_feature = args.optional_feature

# 指定需要提取的列
columns_to_extract = ['bug_id', 'product', 'abstracts', 'description', 'component', 'severity', 'priority', 'developer',  'status','history']
# columns_to_extract = [ 'description', 'developer']
df = pd.read_csv(new_file_path, usecols=columns_to_extract, encoding='latin-1')

# 将developer列作为标签
label_dict = {label: idx for idx, label in enumerate(df['developer'].unique())}
df['label'] = df['developer'].replace(label_dict)
# 合并文本信息为模型的输入，除了developer列
# df['text_input'] = df[['bug_id', 'product', 'abstracts', 'description', 'component', 'severity', 'priority',  'status']].astype(str).agg(' '.join, axis=1)
df['text_input'] =  df['bug_id'].astype(str) + " " + df['component'].astype(str)+ " " + df['abstracts'].astype(str) +" "+ df['severity'].astype(str)+ " "+df['history'].astype(str)  # 使用空格作为分隔符

# df['text_input'] = df[[ 'product',   'component', 'severity', 'priority',  'status','description']].astype(str).agg(' '.join, axis=1)
X_train, X_val, y_train, y_val = train_test_split(df.index.values, df.label.values, test_size=0.15, random_state=42, stratify=df.label.values)
df['data_type'] = ['not_set']*df.shape[0]
df.loc[X_train, 'data_type'] = 'train'
df.loc[X_val, 'data_type'] = 'val'

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

# 对训练和验证数据的合并文本进行编码
encoded_data_train = tokenizer.batch_encode_plus(
    df[df.data_type=='train'].text_input.values,  # 使用合并后的文本
    add_special_tokens=True, 
    return_attention_mask=True, 
    padding='max_length',  # 更新pad_to_max_length为padding
    max_length=512, 
    truncation=True,  # 明确启用截断
    return_tensors='pt'
)

encoded_data_val = tokenizer.batch_encode_plus(
    df[df.data_type=='val'].text_input.values,  # 使用合并后的文本
    add_special_tokens=True, 
    return_attention_mask=True, 
    padding='max_length',  # 更新pad_to_max_length为padding
    max_length=512, 
    truncation=True,  # 明确启用截断
    return_tensors='pt'
)

# 准备Tensor数据
input_ids_train = encoded_data_train['input_ids']
attention_masks_train = encoded_data_train['attention_mask']
labels_train = torch.tensor(df[df.data_type=='train'].label.values)

input_ids_val = encoded_data_val['input_ids']
attention_masks_val = encoded_data_val['attention_mask']
labels_val = torch.tensor(df[df.data_type=='val'].label.values)

dataset_train = TensorDataset(input_ids_train, attention_masks_train, labels_train)
dataset_val = TensorDataset(input_ids_val, attention_masks_val, labels_val)

# 定义DataLoader
batch_size = 4
train_loader = DataLoader(dataset_train, sampler=RandomSampler(dataset_train), batch_size=batch_size)
val_loader = DataLoader(dataset_val, sampler=SequentialSampler(dataset_val), batch_size=32)
# # 初始化模型
# model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(label_dict), output_attentions=False, output_hidden_states=False)
# optimizer = AdamW(model.parameters(), lr=1e-5, eps=1e-8)
# # 加载模型
# # 计算层数
# num_transformer_layers = len(model.bert.encoder.layer)
# print(f'The BERT model has {num_transformer_layers} transformer layers.')
# print(model)
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(label_dict), output_attentions=False, output_hidden_states=False)
optimizer = AdamW(model.parameters(), lr=1e-5, eps=1e-8)
# 加载模型
# 计算层数
num_transformer_layers = len(model.bert.encoder.layer)
print(f'The BERT model has {num_transformer_layers} transformer layers.')
print(model)
# 设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# 检查是否有可用的检查点
if os.path.isfile(checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch'] + 1
    print(f'Resuming training from epoch {start_epoch}')
else:
    start_epoch = 0
    print('Starting training from scratch')

# 训练和验证循环 增加top5 top10
import pymysql
from datetime import datetime

# 数据库连接信息
host = '38.147.173.234'
user = 'lijianye'
password = '660013'
db = 'training_statistics_db'
# 模型名称，根据实际情况手动设置
# 学习率和可选特性，根据实际情况手动设置
learning_rate = 1e-5  # 示例学习率
dataset = new_file_path
num_epochs = 15
for epoch in range(start_epoch, num_epochs):
    model.train()
    start_time = datetime.now()
        
    progress_bar = tqdm(train_loader, desc=f"Epoch {epoch + 1}")
    for batch in progress_bar:
        optimizer.zero_grad()
        input_ids = batch[0].to(device)
        attention_mask = batch[1].to(device)
        labels = batch[2].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs[0]
        loss.backward()
        optimizer.step()
        progress_bar.set_postfix(loss=loss.item())
    torch.save({'epoch': epoch, 'model_state_dict': model.state_dict(), 'optimizer_state_dict': optimizer.state_dict()}, checkpoint_path)
    model.eval()
    correct_topk = {k: 0 for k in range(1, 11)}
    total = 0
    val_progress_bar = tqdm(val_loader, desc="Validating")
    
    for batch in val_progress_bar:
        input_ids = batch[0].to(device)
        attention_mask = batch[1].to(device)
        labels = batch[2].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs[0]
        total += labels.size(0)
        
        # 计算top1到top10的正确率
        _, predicted_topk = torch.topk(logits, k=10, dim=1)
        labels_expanded = labels.unsqueeze(1)
        for k in range(1, 11):
            correct_topk[k] += (predicted_topk[:, :k] == labels_expanded).any(dim=1).sum().item()
                
    # 打印每个topK的准确率
    top10accuracy = []  # 初始化存储Top1到Top10准确率的数组

    for k in range(1, 11):
        accuracy = 100 * correct_topk[k] / total
        top10accuracy.append(accuracy)  # 将计算出的准确率添加到数组中
        print(f'Accuracy after epoch {epoch + 1}: Top{k}: {accuracy:.2f}%')
        print(top10accuracy)
    import pandas as pd
    import os
        # ...训练结束时间
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()/60.0
    # 定义数据字典，用于创建DataFrame
    data = {
            'epoch': [epoch],
            'start_time': [start_time],
            'end_time': [end_time],
            'duration': [duration],
            'user_id': [1],
            'model': [model_name],
            'top1_accuracy': [top10accuracy[0]],
            'top2_accuracy': [top10accuracy[1]],
            'top3_accuracy': [top10accuracy[2]],
            'top4_accuracy': [top10accuracy[3]],
            'top5_accuracy': [top10accuracy[4]],
            'top6_accuracy': [top10accuracy[5]],
            'top7_accuracy': [top10accuracy[6]],
            'top8_accuracy': [top10accuracy[7]],
            'top9_accuracy': [top10accuracy[8]],
            'top10_accuracy': [top10accuracy[9]],
            'optional_feature': [optional_feature],
            'learning_rate': [learning_rate],
            'dataset': [dataset],
            'experiment_num':[experiment_num],
    }

        # 创建DataFrame
    df = pd.DataFrame(data)

        # 检查train.csv文件是否存在来决定是否添加表头
    file_exists = os.path.isfile('modified_train_with_updated_duration.csv')

        # 如果文件存在，不写入表头，模式为追加；如果文件不存在，写入表头，模式为写入
    df.to_csv('xuezhangtrainoutcome.csv', mode='a', header=not file_exists, index=False)

    print(f'Epoch {epoch + 1} training data inserted into train.csv.')