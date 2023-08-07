# sentencepiece
import numpy as np
import pandas as pd
from transformers import AlbertTokenizer, AlbertModel
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch
import torch.nn as nn
import torch.nn.functional as F
import nltk

# Download the English stop words (run this once)
nltk.download('stopwords')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Load Data
true_data = pd.read_csv('true.csv')
fake_data = pd.read_csv('fake.csv')

# Generate labels True/Fake under new Target Column in 'true_data' and 'fake_data'
true_data['Target'] = ['True'] * len(true_data)
fake_data['Target'] = ['Fake'] * len(fake_data)

# Merge 'true_data' and 'fake_data', by random mixing into a single data file
data = pd.concat([true_data, fake_data], ignore_index=True)
data = shuffle(data).reset_index(drop=True)

# changing labels to numbers 0/1 (Fake=1)
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

# Load ALBERT Model and Tokenizer
albert_model_name = 'albert-base-v2'
albert = AlbertModel.from_pretrained(albert_model_name)
tokenizer = AlbertTokenizer.from_pretrained(albert_model_name)

MAX_LENGTH = 15

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove stop words
    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = ' '.join(words)
    return text

def prepare_data(texts, labels):
    # Preprocess the text data
    texts = [preprocess_text(text) for text in texts]
    # Tokenize the preprocessed text
    tokens = tokenizer.batch_encode_plus(
        texts,
        max_length=MAX_LENGTH,
        padding=True,
        truncation=True
    )
    # Convert to numpy arrays
    seq = np.array(tokens['input_ids'])
    mask = np.array(tokens['attention_mask'])
    labelz = np.array(labels.tolist())

    return seq, mask, labelz

# Data Loader structure definition
batch_size = 32

# Prepare the training data
train_seq, train_mask, train_y = prepare_data(train_text, train_labels)
# Prepare the validation data
val_seq, val_mask, val_y = prepare_data(val_text, val_labels)
# Prepare the test data
test_seq, test_mask, test_y = prepare_data(test_text, test_labels)

# Create TensorDatasets and DataLoaders
train_dataset = TensorDataset(torch.tensor(train_seq), torch.tensor(train_mask), torch.tensor(train_y))
train_sampler = RandomSampler(train_dataset)
train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=batch_size)

val_dataset = TensorDataset(torch.tensor(val_seq), torch.tensor(val_mask), torch.tensor(val_y))
val_sampler = SequentialSampler(val_dataset)
val_dataloader = DataLoader(val_dataset, sampler=val_sampler, batch_size=batch_size)

test_dataset = TensorDataset(torch.tensor(test_seq), torch.tensor(test_mask), torch.tensor(test_y))
test_sampler = SequentialSampler(test_dataset)
test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=batch_size)

# Freezing the parameters and defining trainable ALBERT structure
for param in albert.parameters():
    param.requires_grad = False

class ALBERT_Arch(nn.Module):
    def __init__(self, albert):
        super(ALBERT_Arch, self).__init__()
        self.albert = albert
        self.dropout = nn.Dropout(0.1)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(768, 512)  # Update the input size to 768
        self.fc2 = nn.Linear(512, 2)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
        cls_hs = self.albert(sent_id, attention_mask=mask)['pooler_output']  # Use 'pooler_output' for ALBERT
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

model = ALBERT_Arch(albert)  # Use the ALBERT-based architecture

# Defining the hyperparameters (optimizer, weights of the classes and the epochs)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5, weight_decay=0.15)  # Added L2 regularization (weight_decay)
cross_entropy = nn.NLLLoss()
epochs = 2

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
        torch.save(model.state_dict(), 'model_weights1.pt')

    train_losses.append(train_loss)
    valid_losses.append(valid_loss)

    print(f'\nTraining Loss: {train_loss:.3f}')
    print(f'Validation Loss: {valid_loss:.3f}')

# Load the best model for evaluation
model.load_state_dict(torch.load('model_weights1.pt'))

model.eval()
with torch.no_grad():
    preds = []
    for step, batch in enumerate(val_dataloader):
        batch = [t.to(device) for t in batch]
        sent_id, mask, labels = batch
        predictions = model(sent_id, mask)
        predictions = torch.argmax(predictions, axis=1)
        preds.extend(predictions.cpu().numpy())

# Evaluate and print classification report
print(classification_report(val_y, preds))
