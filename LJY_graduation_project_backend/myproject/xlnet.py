import argparse
import os
import torch
from tqdm.auto import tqdm
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from transformers import XLNetTokenizer, XLNetForSequenceClassification, AdamW

# 设置命令行参数
parser = argparse.ArgumentParser(description="XLNet Model Training")
parser.add_argument('--new_file_path', type=str, default='./dataset2/OpenOffice_total_10_10.csv', help='Path to the dataset file')
parser.add_argument('--checkpoint_path', type=str, default='model_checkpoint_xlnet_top1-top10_eclipse_dataprocessed4444444OpenOffice_total_10_10.pth', help='Path to the model checkpoint file')
parser.add_argument('--experiment_num', type=int, default=13, help='Experiment number')
parser.add_argument('--model_name', type=str, default='xlnet', help='Name of the model')
parser.add_argument('--optional_feature', type=str, default='abstract+description', help='Optional features used')
args = parser.parse_args()

# 使用命令行参数
new_file_path = args.new_file_path
checkpoint_path = args.checkpoint_path
experiment_num = args.experiment_num
model_name = args.model_name
optional_feature = args.optional_feature

# 加载数据
df = pd.read_csv(new_file_path, usecols=['bug_id', 'product', 'abstracts', 'description', 'component', 'severity', 'priority', 'developer', 'status'], encoding='latin-1')
label_dict = {label: idx for idx, label in enumerate(df['developer'].unique())}
df['label'] = df['developer'].replace(label_dict).infer_objects()
df['text_input'] = df['abstracts'].astype(str) + " " + df['description'].astype(str)
X_train, X_val, y_train, y_val = train_test_split(df.index.values, df.label.values, test_size=0.15, random_state=42, stratify=df.label.values)
df['data_type'] = ['not_set']*df.shape[0]
df.loc[X_train, 'data_type'] = 'train'
df.loc[X_val, 'data_type'] = 'val'

# 使用XLNet的分词器
tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
encoded_data_train = tokenizer.batch_encode_plus(
    df[df.data_type=='train'].text_input.values,
    add_special_tokens=True,
    return_attention_mask=True,
    padding='max_length',
    truncation=True,
    max_length=512,
    return_tensors='pt'
)
encoded_data_val = tokenizer.batch_encode_plus(
    df[df.data_type=='val'].text_input.values,
    add_special_tokens=True,
    return_attention_mask=True,
    padding='max_length',
    truncation=True,
    max_length=512,
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
batch_size = 2
train_loader = DataLoader(dataset_train, sampler=RandomSampler(dataset_train), batch_size=batch_size)
val_loader = DataLoader(dataset_val, sampler=SequentialSampler(dataset_val), batch_size=32)

# 初始化XLNet模型
model = XLNetForSequenceClassification.from_pretrained("xlnet-base-cased", num_labels=len(label_dict))
optimizer = AdamW(model.parameters(), lr=1e-5, eps=1e-8)
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