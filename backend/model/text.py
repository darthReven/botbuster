import re

def chunkBySentences(text):
    '''Pattern Breakdown:
    (?<!\w\.\w): Ensures that periods [.] are not preceded and/or succeeded by another period or word character, helps to identify abbreviations such as 'Mr.', 'e.g.', 'etc.'
    (?<![A-Z][a-z]\.): Checks that periods [.] are not preceded by an uppercase letter, lowercase letter and another period, helps to identify initialisations like 'A.S.A.P.'
    (?<=\.|\?|\!)\s: Matches [. ? !] that marks the end of a sentence and any whitespace that follows it
    \s*: Removes whitespaces
    '''
    pattern = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s*"
    sentences = re.split(pattern, text.strip())
    if sentences[-1] == "":
        sentences = sentences[:-1]
    return sentences

def chunkByParagraphs(text):
    '''Pattern Breakdown:
    \n{1,}: Matches one or more consecutive newline characters
    \s*: Removes whitespaces
    '''
    pattern = r"\s*\n{1,}\s*"
    paragraphs = re.split(pattern, text.strip())
    return paragraphs

def chunkByCharacterLimit(text):
    limit = 400
    sentences = chunkBySentences(text)
    chunks = []
    chunkCheck = ''

    for i in sentences:
        if len(chunkCheck) + len(i) <= limit:
            if chunkCheck:
                chunkCheck += ' ' + i.strip()
            else:
                chunkCheck = i.strip()
        else:
            chunks.append(chunkCheck)
            chunkCheck = i.strip()

    chunks.append(chunkCheck)
    return chunks

input_sentence = '''Apples, scientifically known as Malus domestica, are one of the most widely cultivated and consumed fruits around the world. They belong to the Rosaceae family, which also includes other fruits like pears, peaches, and cherries. Apples are known for their distinctive shape, crisp texture, and a wide range of flavors ranging from sweet to tart.
There are thousands of apple varieties grown globally, each with its unique characteristics. Some popular apple varieties include Granny Smith, Gala, Red Delicious, Fuji, and Honeycrisp. These varieties differ in color, taste, texture, and even their best usage. For example, Granny Smith apples are known for their bright green color, tartness, and excellent baking qualities, while Gala apples have a sweeter taste and are often enjoyed fresh.
Apples are not only delicious but also highly nutritious. They are a great source of dietary fiber, antioxidants, and essential vitamins and minerals. Eating apples regularly can contribute to improved digestive health, reduced risk of chronic diseases, and boosted immune function. Apples are also low in calories and fat, making them a healthy snack option for weight management.
Besides their nutritional benefits, apples have cultural significance and are often associated with traditions and folklore. They have been featured in various legends, stories, and even religious references throughout history. In many cultures, apples symbolize knowledge, temptation, and vitality.
Apples are versatile and can be enjoyed in various ways. They can be eaten fresh, sliced in salads, or used as an ingredient in both sweet and savory dishes. Apples are commonly used in baking, where they add natural sweetness and moisture to cakes, pies, and muffins. They can also be made into applesauce, apple cider, or apple juice.
The apple industry plays a significant role in many economies, especially in regions with favorable climates for apple cultivation. The cultivation of apple trees requires specific growing conditions, including the right amount of sunlight, well-drained soil, and proper care to ensure healthy tree growth and optimal fruit production.
Harvesting apples usually takes place in the late summer or early fall, depending on the apple variety and location. Apples are typically picked by hand to ensure they are at their peak ripeness. Once harvested, they can be stored for several months under controlled conditions, allowing them to be available throughout the year.
In conclusion, apples are not just a popular and delicious fruit; they also offer a range of health benefits and cultural significance. With their diverse varieties, nutritional value, and versatility in culinary applications, apples continue to be a favorite fruit enjoyed by people of all ages.'''

chunked = chunkByCharacterLimit(input_sentence)
for chunk in chunked:
    print(chunk)