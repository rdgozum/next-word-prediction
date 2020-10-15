# Import required libraries
import torch
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class GPT2:
    def __init__(self):
        super(GPT2, self).__init__()

        self.model_type = "GPT2"

        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        # Load pre-trained model (weights)
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")

    def predict_next(self, text, k):
        # Encode a text inputs
        indexed_tokens = self.tokenizer.encode(text)

        # Convert indexed tokens in a PyTorch tensor
        tokens_tensor = torch.tensor([indexed_tokens])

        # Set the model in evaluation mode to deactivate the DropOut modules
        self.model.eval()

        # If you have a GPU, put everything on cuda
        tokens_tensor = tokens_tensor.to(device)
        self.model.to(device)

        # Predict all tokens
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]

        # Get the predicted next sub-word
        probs = predictions[0, -1, :]
        top_next = [self.tokenizer.decode(i.item()).strip() for i in probs.topk(k)[1]]

        return top_next
