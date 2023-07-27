# THIS FILE IS NOT CALLED BY THE API, IT IS PURELY USED TO TRAIN THE MODEL AND SAVE ITS WEIGHTS
import numpy as np
import pandas as pd
from transformers import AutoModel, BertTokenizerFast
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch
import torch.nn as nn
import torch.nn.functional as F

true_data = pd.read_csv('true.csv')
fake_data = pd.read_csv('fake.csv')

# Generate labels True/Fake under new Target Column in 'true_data' and 'fake_data'
true_data['Target'] = ['True'] * len(true_data)
fake_data['Target'] = ['Fake'] * len(fake_data)

# Merge 'true_data' and 'fake_data', by random mixing into a single df called 'data'
data = pd.concat([true_data, fake_data], ignore_index=True)
data = shuffle(data).reset_index(drop=True)

# sample some data from the dataset to reduce training time for now can remove ltr i think
data = data.sample(n=15000, random_state=42)
# Target column is made of string values True/Fake, let's change it to numbers 0/1 (Fake=1)
data['label'] = pd.get_dummies(data.Target)['Fake']

# Train-Validation-Test set split into 70:15:15 ratio
train_text, temp_text, train_labels, temp_labels = train_test_split(
    data['title'],
    data['label'],
    random_state=2018,
    test_size=0.3,
    stratify=data['Target']
)

val_text, test_text, val_labels, test_labels = train_test_split(
    temp_text,
    temp_labels,
    random_state=2018,
    test_size=0.5,
    stratify=temp_labels
)

bert_model_name = 'bert-base-uncased'
bert = AutoModel.from_pretrained(bert_model_name)
tokenizer = BertTokenizerFast.from_pretrained(bert_model_name)

MAX_LENGTH = 15

tokens_train = tokenizer.batch_encode_plus(
    train_text.tolist(),
    max_length=MAX_LENGTH,
    padding=True,  # Updated argument name
    truncation=True
)

tokens_val = tokenizer.batch_encode_plus(
    val_text.tolist(),
    max_length=MAX_LENGTH,
    padding=True,  # Updated argument name
    truncation=True
)

tokens_test = tokenizer.batch_encode_plus(
    test_text.tolist(),
    max_length=MAX_LENGTH,
    padding=True,  # Updated argument name
    truncation=True
)

train_seq = np.array(tokens_train['input_ids'])
train_mask = np.array(tokens_train['attention_mask'])
train_y = np.array(train_labels.tolist())

val_seq = np.array(tokens_val['input_ids'])
val_mask = np.array(tokens_val['attention_mask'])
val_y = np.array(val_labels.tolist())

test_seq = np.array(tokens_test['input_ids'])
test_mask = np.array(tokens_test['attention_mask'])
test_y = np.array(test_labels.tolist())

# Data Loader structure definition
batch_size = 32

train_dataset = TensorDataset(torch.tensor(train_seq), torch.tensor(train_mask), torch.tensor(train_y))
train_sampler = RandomSampler(train_dataset)
train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=batch_size)

val_dataset = TensorDataset(torch.tensor(val_seq), torch.tensor(val_mask), torch.tensor(val_y))
val_sampler = SequentialSampler(val_dataset)
val_dataloader = DataLoader(val_dataset, sampler=val_sampler, batch_size=batch_size)

# Freezing the parameters and defining trainable BERT structure
for param in bert.parameters():
    param.requires_grad = False

class BERT_Arch(nn.Module):
    def __init__(self, bert):
        super(BERT_Arch, self).__init__()
        self.bert = bert
        self.dropout = nn.Dropout(0.1)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(768, 512)
        self.fc2 = nn.Linear(512, 2)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
        cls_hs = self.bert(sent_id, attention_mask=mask)['pooler_output']
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

model = BERT_Arch(bert)

# Defining the hyperparameters (optimizer, weights of the classes and the epochs)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)
cross_entropy = nn.NLLLoss()
epochs = 1

# Training and Evaluation Functions
def train():
    model.train()
    total_loss = 0

    for step, batch in enumerate(train_dataloader):
        batch = [r.to(device) for r in batch]
        sent_id, mask, labels = batch
        model.zero_grad()
        preds = model(sent_id, mask)
        labels = labels.to(torch.int64)  # Convert labels to torch.int64
        loss = cross_entropy(preds, torch.LongTensor(labels).to(device))
        total_loss += loss.item()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

    avg_loss = total_loss / len(train_dataloader)
    return avg_loss

def evaluate():
    model.eval()
    total_loss = 0

    for step, batch in enumerate(val_dataloader):
        batch = [t.to(device) for t in batch]
        sent_id, mask, labels = batch
        with torch.no_grad():
            preds = model(sent_id, mask)
            labels = labels.to(torch.int64)  # Convert labels to torch.int64
            loss = cross_entropy(preds, torch.LongTensor(labels).to(device))
            total_loss += loss.item()

    avg_loss = total_loss / len(val_dataloader)
    return avg_loss


# Training Loop
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

best_valid_loss = float('inf')
train_losses = []
valid_losses = []

for epoch in range(epochs):
    print('\nEpoch {:} / {:}'.format(epoch + 1, epochs))
    train_loss = train()
    valid_loss = evaluate()

    if valid_loss < best_valid_loss:
        best_valid_loss = valid_loss
        torch.save(model.state_dict(), 'new_model_weights.pt')

    train_losses.append(train_loss)
    valid_losses.append(valid_loss)

    print(f'\nTraining Loss: {train_loss:.3f}')
    print(f'Validation Loss: {valid_loss:.3f}')

# Load the best model for evaluation
model.load_state_dict(torch.load('new_model_weights.pt'))

# Testing and Predicting (OPTIONAL)
with torch.no_grad():
    preds = model(torch.tensor(test_seq).to(device), torch.tensor(test_mask).to(device))
    preds = preds.detach().cpu().numpy()

preds = np.argmax(preds, axis=1)
print(classification_report(test_y, preds))