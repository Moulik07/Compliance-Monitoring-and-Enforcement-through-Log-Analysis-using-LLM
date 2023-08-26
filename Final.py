from transformers import GPT2LMHeadModel, GPT2TokenizerFast

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2TokenizerFast.from_pretrained(model_name)

# Placeholder file paths for compliance rules and system logs
compliance_rules_file = "path/to/compliance/rules.txt"
system_logs_file = "path/to/system/logs.txt"

# Load compliance rules and system logs
with open(compliance_rules_file, "r") as f:
    compliance_rules = f.read()

with open(system_logs_file, "r") as f:
    system_logs = f.read()

# Combine compliance rules and system logs for context
input_text = f"Compliance Rules:\n{compliance_rules}\nSystem Logs:\n{system_logs}\n"

# Tokenize input text
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate compliance breach report
max_length = 300  # Adjust as needed
num_return_sequences = 1
generated_text = model.generate(input_ids, max_length=max_length, num_return_sequences=num_return_sequences)

# Decode and print generated report
generated_report = tokenizer.decode(generated_text[0], skip_special_tokens=True)
print("Generated Compliance Breach Report:\n")
print(generated_report)
