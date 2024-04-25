import os

def save_rule(rule_content, rule_name, output_dir):
    filename = f"{rule_name.replace(' ', '_').replace(':', '_')}.yar"
    with open(os.path.join(output_dir, filename), 'w') as file:
        file.write(''.join(rule_content))

def parse_forge(input_file, output_dir):
# Parsing the combined file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r') as file:
        rule_content = []
        rule_name = None
        comment_block = False

        for line in file:
            line = line.strip()

            if line.strip().startswith('/*'):
                comment_block = True
            if line.strip().endswith('*/'):
                comment_block = False
                continue

            if comment_block or line.strip() == '':
                continue

            if line.startswith('rule '):
                if rule_content:
                    save_rule(rule_content, rule_name, output_dir)
                    rule_content = []
                rule_name = line.split()[1].split(':')[0]
                rule_content.append(line)
            elif rule_content:
                rule_content.append(line)

        if rule_content:
            save_rule(rule_content, rule_name, output_dir)


if __name__ == '__main__':
    input_file = './yara-rules-core.yar'
    output_dir = './yara_rules/'
    parse_forge(input_file, output_dir)
    print(f"Yara rules parsed and saved into individual files under {output_dir}")
