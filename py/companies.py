import json
import random
import string

def generate_chinese_company_name():
    # 使用常见的中文字符来生成公司名称
    prefixes = ['优创', '合力', '同创', '新时代', '高新', '宝安', '江南', '东方', '昌盛', '永康']
    suffixes = ['科技', '电子', '信息', '贸易', '实业', '网络', '文化', '制药', '设备', '食品']
    return random.choice(prefixes) + random.choice(suffixes) + '有限公司'

def generate_company():
    company = {}
    company['name'] = generate_chinese_company_name()
    company['type'] = random.choice(['科技', '金融', '制造', '医疗', '零售'])
    company['size'] = random.choice(['小型', '中型', '大型'])
    # 随机生成数字和汉字结合的地址
    street_names = ['长安街', '建国路', '人民路', '和平路', '中山路']
    company['address'] = random.choice(street_names) + str(random.randint(1, 1000)) + '号'
    company['founded'] = f"{random.randint(1980, 2022)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    company['business_area'] = random.choice(['软件开发', '金融服务', '汽车制造', '制药', '电子商务'])
    return company

def generate_relationships(companies):
    relationships = []
    for i in range(len(companies)):
        for j in range(i+1, len(companies)):
            if random.random() < 0.3:  # Randomly decide if there is a relationship
                relationships.append({'source': companies[i]['name'], 'target': companies[j]['name']})
    return relationships

if __name__ == '__main__':
    companies = [generate_company() for _ in range(20)]
    relationships = generate_relationships(companies)

    data = {'companies': companies, 'relationships': relationships}

    with open('company_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("数据已生成并保存至 company_data.json。")
