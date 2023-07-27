import numpy as np
import pandas as pd
from transformers import AutoModel, BertTokenizerFast
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch
import torch.nn as nn
import torch.nn.functional as F

# Load the true and fake data from CSV files
true_data = pd.read_csv('true.csv')
fake_data = pd.read_csv('fake.csv')

# Generate labels True/Fake under new Target Column in 'true_data' and 'fake_data'
true_data['Target'] = ['True'] * len(true_data)
fake_data['Target'] = ['Fake'] * len(fake_data)

# Merge 'true_data' and 'fake_data', by random mixing into a single df called 'data'
data = pd.concat([true_data, fake_data]).sample(frac=1, random_state=42).reset_index(drop=True)

# Change the target column to numbers (Fake=1)
data['label'] = pd.get_dummies(data.Target)['Fake']

# Randomly sample about 10,000 data points from the dataset
num_samples = 10000
data_sampled = data.sample(n=num_samples, random_state=42)

# Train-Validation-Test set split into 70:15:15 ratio on the sampled data
train_text, temp_text, train_labels, temp_labels = train_test_split(
    data_sampled['title'],
    data_sampled['label'],
    random_state=2018,
    test_size=0.3,
    stratify=data_sampled['Target']
)

val_text, test_text, val_labels, test_labels = train_test_split(
    temp_text,
    temp_labels,
    random_state=2018,
    test_size=0.5,
    stratify=temp_labels
)

bert = AutoModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

MAX_LENGTH = 15
# Tokenize and encode sequences in the train set
tokens_train = tokenizer.batch_encode_plus(
    train_text.tolist(),
    max_length=MAX_LENGTH,
    padding=True,  # Use padding='max_length' to pad to the maximum length in the batch
    truncation=True
)

train_seq = torch.tensor(tokens_train['input_ids'])
train_mask = torch.tensor(tokens_train['attention_mask'])
train_y = torch.tensor(train_labels.tolist())

# Tokenize and encode sequences in the validation set
tokens_val = tokenizer.batch_encode_plus(
    val_text.tolist(),
    max_length=MAX_LENGTH,
    padding=True,  # Use padding='max_length' to pad to the maximum length in the batch
    truncation=True
)

val_seq = torch.tensor(tokens_val['input_ids'])
val_mask = torch.tensor(tokens_val['attention_mask'])
val_y = torch.tensor(val_labels.tolist())

# Tokenize and encode sequences in the test set
tokens_test = tokenizer.batch_encode_plus(
    test_text.tolist(),
    max_length=MAX_LENGTH,
    padding=True,  # Use padding='max_length' to pad to the maximum length in the batch
    truncation=True
)

test_seq = torch.tensor(tokens_test['input_ids'])
test_mask = torch.tensor(tokens_test['attention_mask'])
test_y = torch.tensor(test_labels.tolist())

# Define batch_size
batch_size = 32

# Data Loader structure definition on the sampled data
train_dataset = TensorDataset(train_seq, train_mask, train_y)
train_sampler = RandomSampler(train_dataset)
train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=batch_size)

val_dataset = TensorDataset(val_seq, val_mask, val_y)
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

# Create an instance of the BERT_Arch class
model = BERT_Arch(bert)

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Define the optimizer and loss function
optimizer = torch.optim.Adam(params=model.parameters(), lr=2e-5)
cross_entropy = nn.CrossEntropyLoss()

# Define the number of training epochs
epochs = 1

# Training Loop with sampled data
best_valid_loss = float('inf')
train_losses = []
valid_losses = []

def train():
    model.train()
    total_loss, total_accuracy = 0, 0

    for step, batch in enumerate(train_dataloader):
        # Unpack batch
        sent_id, mask, labels = batch
        # Move tensors to the configured device
        sent_id, mask, labels = sent_id.to(device), mask.to(device), labels.to(device)

        # Clear previously calculated gradients
        model.zero_grad()

        # Perform forward pass and compute logits
        preds = model(sent_id, mask)

        # Compute the loss
        loss = cross_entropy(preds, labels)

        # Backpropagation
        loss.backward()

        # Clip the norm of the gradients to 1.0 to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        # Update parameters and take a step using the computed gradient
        optimizer.step()

        # Update tracking variables
        total_loss += loss.item()

        # Move logits and labels to CPU
        preds = preds.detach().cpu().numpy()
        label_ids = labels.to('cpu').numpy()

        # Calculate accuracy
        total_accuracy += flat_accuracy(preds, label_ids)

    # Compute the average loss and average accuracy over all batches
    avg_loss = total_loss / len(train_dataloader)
    avg_accuracy = total_accuracy / len(train_dataloader)

    train_losses.append(avg_loss)

    print(f"Train loss: {avg_loss:.4f}, Train Accuracy: {avg_accuracy:.4f}")

    return avg_loss

# Training Loop
for epoch in range(epochs):
    train_loss=train()
    # ... (Rest of the training loop as defined in your previous code)

# ... (Rest of the code as defined in your previous code)

# Load the best model for evaluation
model.load_state_dict(torch.load('new_model_weights.pt'))

# Testing and Predicting (OPTIONAL)
with torch.no_grad():
    preds = model(test_seq.to(device), test_mask.to(device))
    preds = preds.detach().cpu().numpy()

preds = np.argmax(preds, axis=1)
print(classification_report(test_y.cpu(), preds))
