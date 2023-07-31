# run with py ./main.py
from transformers import AlbertModel, AlbertTokenizerFast
import torch
import torch.nn as nn
from fastapi import FastAPI
from pydantic import BaseModel

# importing the model from the saved weights
class ALBERT_Arch(nn.Module):
    def __init__(self, albert_model_name):
        super(ALBERT_Arch, self).__init__()
        self.albert = AlbertModel.from_pretrained(albert_model_name)
        self.dropout = nn.Dropout(0.1)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(768, 512)  # Adjust the input size to 768 for ALBERT
        self.fc2 = nn.Linear(512, 2)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
        cls_hs = self.albert(sent_id, attention_mask=mask)['pooler_output']
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

def load_and_tokenize(albert_model_name, text, max_length=15):
    tokenizer = AlbertTokenizerFast.from_pretrained(albert_model_name)
    tokens = tokenizer.batch_encode_plus(
        [text],
        max_length=max_length,
        padding=True,
        truncation=True
    )

    seq = torch.tensor(tokens['input_ids'])
    mask = torch.tensor(tokens['attention_mask'])

    return seq, mask

def predict_text(albert_model_name, model, seq, mask, device="cpu"):
    model.to(device)
    model.eval()

    with torch.no_grad():
        preds = model(seq.to(device), mask.to(device))
        prob_fake_class = torch.softmax(preds, dim=1)[:, 1].item()  # Get the probability of the "Fake" class (class 1)

    return prob_fake_class

# Function to predict whether the text is fake or real
def predictText(text):
    seq, mask = load_and_tokenize(albert_model_name, text)
    prediction = predict_text(albert_model_name, model, seq, mask)
    return prediction

albert_model_name = 'albert-base-v2'
model = ALBERT_Arch(albert_model_name)

# Load the pre-trained model weights
model.load_state_dict(torch.load('new_model_weights1.pt'))

# print(predictText("The Straits Times is an English-language daily broadsheet newspaper based in Singapore and currently owned by SPH Media Trust. The Sunday Times is its Sunday edition. The newspaper was established on 15 July 1845 as The Straits Times and Singapore Journal of Commerce."))
# here is where the actual api shit starts

misinfo=FastAPI()
class Text(BaseModel):
    text: str

@misinfo.post("/predict/")
def predict(text: Text):
    # print(text)
    predText = text.dict()["text"]
    prediction=predictText(predText)
    return({"prediction": prediction})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(misinfo, host="0.0.0.0", port=8001)