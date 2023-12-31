import json
from tqdm import tqdm
from fire import Fire

def extract_conversation(data, keys, remove_extra_markers=False):
    prompt = ''
    for key in keys[0][1:-1].split("+"):
        if 'user' not in key.lower():
            if remove_extra_markers and 'gpt' in key.lower():
                continue
            prompt += data[key] + '\n'
    assert 'gpt' in keys[1].lower(), keys[1] 
    response = data[keys[1]]
    return prompt, response

def convert(in_file, out_file, remove_extra_markers=False):
    with open(in_file, "r") as f:
        dataset = []
        for row in tqdm(f, desc="Generate a new dataset"):
            data = json.loads(row)
            new_data = {}
            history = []
            keys = data['fields'].split(",")
            assert len(keys)%3 == 0, keys
            for i in range(len(keys)//3):
                
                if len(keys) > 3 and i < len(keys)//3-1:
                    prompt, response = extract_conversation(data, keys[3*i:3*i+3], remove_extra_markers=remove_extra_markers)
                    history.append((prompt, response))
                else:
                    prompt, response = extract_conversation(data, keys[3*i:3*i+3], remove_extra_markers=False)
            new_data['prompt'] = prompt
            new_data['response'] = response
            new_data['history'] = history
            dataset.append(new_data)

    with open(out_file, "w") as f:
        for data in tqdm(dataset, desc="Saving the new dataset"):
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    Fire(convert)