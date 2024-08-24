import torch
from tqdm import tqdm

# Initialize a dictionary with dummy layers (LoRA-like weights)
dict_lora = {
    'layer1': torch.nn.Linear(10, 5),
    'layer2': torch.nn.Linear(5, 2),
    'layer3': torch.nn.Linear(2, 1)
}

# Print original weights
print("Original weights:")
for k, v in dict_lora.items():
    print(f"{k} weights before update:\n", v.weight)

# Create a tensor to be used for copying (same size as weights in the layers)
# Here I'm using a tensor filled with ones, but in practice, you'd use something meaningful
for k, v in dict_lora.items():
    tensor = torch.ones_like(v.weight)

    # Copy the tensor's values into the weights of the layers
    with torch.no_grad():
        v.weight.copy_(tensor)

# Print updated weights
print("\nUpdated weights:")
for k, v in dict_lora.items():
    print(f"{k} weights after update:\n", v.weight)
