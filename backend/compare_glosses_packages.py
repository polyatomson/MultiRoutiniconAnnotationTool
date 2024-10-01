import json
import os.path

def merge_packages(new_fn: str, main_fn: str='glosses_starter_package.json', merged_name: str='glosses_starter_package'):
    with open(main_fn, 'r') as f:
        main_package = json.load(f)["glosses"]
    
    with open(new_fn, 'r') as f:
        new_package = json.load(f)["glosses"]
    to_add = list()
    for gloss in new_package:
        already = False
        for old_gloss in main_package:
            if gloss["gloss"] == old_gloss["gloss"] and gloss["lex"] == old_gloss["lex"]:
                already = True
                break
        if not already:
            to_add.append(gloss)
    main_package.extend(to_add)
    merged = {"glosses":main_package}
    output_name = merged_name+'.json'
    exists = os.path.isfile(output_name)
    if exists:
        suffix = 0
        while exists:
            suffix += 1
            output_name = merged_name+str(suffix)+'.json'
            exists = os.path.isfile(output_name)
    
    with open(output_name, 'w') as f:
        json.dump(merged, f, indent=3)
    
    print('N glosses added:', str(len(to_add)))

def main():
    input_fn = input('which file should I add to the starter package? ')
    merge_packages(input_fn)    

if __name__ == '__main__':
    main()

# multpragmaticon_glosses_202402131712.json
