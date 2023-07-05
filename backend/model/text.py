import nltk
import re

# nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def chunk_by_sentences(text):
    sentences = sent_tokenize(text)
    joined = []
    abbreviations = ['e.g.', 'i.e.']
    sentence = 0

    while sentence < len(sentences):
        if sentences[sentence].endswith(tuple(abbreviations)) and sentence + 1 < len(sentences):
            # Manually join sentences with abbrevations [e.g., i.e.] since nltk only caters for them with commas
            joined.append(sentences[sentence] + ' ' + sentences[sentence + 1])
            # Skip the next sentence since it was joined
            sentence += 2  
        else:
            joined.append(sentences[sentence])
            sentence += 1

    return joined

def chunk_by_paragraphs(text):
    '''Pattern Breakdown:
    \n{1,}: Matches one or more consecutive newline characters
    \s*: Removes whitespaces
    '''
    pattern = r"\s*\n{1,}\s*"
    paragraphs = re.split(pattern, text.strip())
    return paragraphs

def chunk(text:str, chunk_option, threshold:int  = 2000):
    chunks = []
    current_chunk = []
    total_chars = 0

    def process_chunks(chunks_to_process):
        nonlocal current_chunk, total_chars
        # avg_chunk_size = len(text) / max(len(chunks_to_process), 1) # not needed
        print(f"len(chunks_to_process) {len(chunks_to_process)}")

        for chunk in chunks_to_process:
            chunk_length = len(chunk)
            # Determines if length of current chunk exceeds threshold
            if total_chars + chunk_length > threshold:
                # Register current chunk to the list of chunks before starting a new chunk with the current sentence
                chunks.append([' '.join(current_chunk)])
                current_chunk = [chunk]
                total_chars = 0 

            else:
                # Append sentence to current chunk if total character length is less than or equal to 1500
                current_chunk.append(chunk)
                total_chars += chunk_length
              
        # Append last chunk to list of chunks
        if current_chunk:
            if chunk_option == 'paragraphs':
                chunks.append([' '.join(current_chunk)])
                current_chunk = []
                total_chars = 0

            else:
                chunks.append(current_chunk)

    if chunk_option == 'sentences':
        sentences = chunk_by_sentences(text) # Split text into sentences
        process_chunks(sentences)
    
    elif chunk_option == 'paragraphs':
        paragraphs = chunk_by_paragraphs(text) # Split text into paragraphs
        for paragraph in paragraphs:
            sentences_in_paragraphs = chunk_by_sentences(paragraph)
            process_chunks(sentences_in_paragraphs)
    else:
        raise ValueError("Invalid Chunk Option")
    
    return chunks

# input_text = '''The tale of Adam and Eve is one of the most enduring and well-known narratives in human history. 
# It is a story that explores the origins of humanity and carries profound symbolic significance. According to the biblical account, Adam and Eve were the first human beings created by God, placed in the Garden of Eden, a paradise of unimaginable beauty and perfection. In this idyllic setting, Adam and Eve lived in harmony with nature, enjoying the bountiful fruits of the garden. They were free to explore and tend to the land, and their only commandment was to abstain from eating the fruit of the Tree of Knowledge of Good and Evil. However, temptation would soon find its way into their lives in the form of a cunning serpent. The serpent, driven by its own desires, enticed Eve to eat the forbidden fruit, promising her enlightenment and wisdom. Eve, enticed by the prospect of gaining knowledge, succumbed to temptation and ate the fruit. She then shared it with Adam, who also partook, thus defying the commandment of God. Their act of disobedience had profound consequences. Suddenly, they became aware of their nakedness and experienced shame. They were banished from the Garden of Eden, condemned to a life of toil and hardship. The harmony they once enjoyed was shattered, and they were thrust into a world of pain, suffering, and mortality. The story of Adam and Eve raises numerous philosophical and theological questions. It explores the nature of human free will and the consequences of moral choices. It delves into the concept of temptation and the fragility of human nature. It also highlights the tension between human desires and divine commands, and the consequences of disobeying those commands. Furthermore, the tale of Adam and Eve can be interpreted as a metaphorical representation of the human condition. It symbolizes the loss of innocence and the entry of humanity into a world of moral complexity. It speaks to the universal human experience of grappling with desires, making choices, and facing the repercussions of those choices. Despite their disobedience, the story of Adam and Eve also contains elements of hope and redemption. God, in His mercy, provides them with garments to cover their nakedness and promises a future Savior who would ultimately reconcile humanity with the divine. This foreshadows the central message of Christianity, the belief in Jesus Christ as the redeemer who would bring salvation to all. The tale of Adam and Eve continues to captivate and resonate with people across different cultures and religions. It serves as a cautionary tale, reminding us of the consequences of yielding to temptation and the importance of moral choices. It invites us to reflect on the complexities of human nature and the pursuit of knowledge. Ultimately, it encourages us to seek redemption and strive for spiritual growth. In conclusion, the story of Adam and Eve is a profound narrative that explores the origins of humanity and grapples with fundamental questions about human nature, free will, and the consequences of choices. It serves as a powerful metaphor for the human condition and carries enduring lessons for individuals and societies alike.It is a story that explores the origins of humanity and carries profound symbolic significance. According to the biblical account, Adam and Eve were the first human beings created by God, placed in the Garden of Eden, a paradise of unimaginable beauty and perfection. In this idyllic setting, Adam and Eve lived in harmony with nature, enjoying the bountiful fruits of the garden. They were free to explore and tend to the land, and their only commandment was to abstain from eating the fruit of the Tree of Knowledge of Good and Evil. However, temptation would soon find its way into their lives in the form of a cunning serpent. The serpent, driven by its own desires, enticed Eve to eat the forbidden fruit, promising her enlightenment and wisdom. Eve, enticed by the prospect of gaining knowledge, succumbed to temptation and ate the fruit. She then shared it with Adam, who also partook, thus defying the commandment of God. Their act of disobedience had profound consequences. Suddenly, they became aware of their nakedness and experienced shame. They were banished from the Garden of Eden, condemned to a life of toil and hardship. The harmony they once enjoyed was shattered, and they were thrust into a world of pain, suffering, and mortality. The story of Adam and Eve raises numerous philosophical and theological questions. It explores the nature of human free will and the consequences of moral choices. It delves into the concept of temptation and the fragility of human nature. It also highlights the tension between human desires and divine commands, and the consequences of disobeying those commands. Furthermore, the tale of Adam and Eve can be interpreted as a metaphorical representation of the human condition. It symbolizes the loss of innocence and the entry of humanity into a world of moral complexity. It speaks to the universal human experience of grappling with desires, making choices, and facing the repercussions of those choices. Despite their disobedience, the story of Adam and Eve also contains elements of hope and redemption. God, in His mercy, provides them with garments to cover their nakedness and promises a future Savior who would ultimately reconcile humanity with the divine. This foreshadows the central message of Christianity, the belief in Jesus Christ as the redeemer who would bring salvation to all. The tale of Adam and Eve continues to captivate and resonate with people across different cultures and religions. It serves as a cautionary tale, reminding us of the consequences of yielding to temptation and the importance of moral choices. It invites us to reflect on the complexities of human nature and the pursuit of knowledge. Ultimately, it encourages us to seek redemption and strive for spiritual growth. In conclusion, the story of Adam and Eve is a profound narrative that explores the origins of humanity and grapples with fundamental questions about human nature, free will, and the consequences of choices. It serves as a powerful metaphor for the human condition and carries enduring lessons for individuals and societies alike. Despite their disobedience, the story of Adam and Eve also contains elements of hope and redemption. God, in His mercy, provides them with garments to cover their nakedness and promises a future Savior who would ultimately reconcile humanity with the divine. This foreshadows the central message of Christianity, the belief in Jesus Christ as the redeemer who would bring salvation to all. The tale of Adam and Eve continues to captivate and resonate with people across different cultures and religions. It serves as a cautionary tale, reminding us of the consequences of yielding to temptation and the importance of moral choices. It invites us to reflect on the complexities of human nature and the pursuit of knowledge. Ultimately, it encourages us to seek redemption and strive for spiritual growth. In conclusion, the story of Adam and Eve is a profound narrative that explores the origins of humanity and grapples with fundamental questions about human nature, free will, and the consequences of choices. It serves as a powerful metaphor for the human condition and carries enduring lessons for individuals and societies alike.It is a story that explores the origins of humanity and carries profound symbolic significance. According to the biblical account, Adam and Eve were the first human beings created by God, placed in the Garden of Eden, a paradise of unimaginable beauty and perfection. In this idyllic setting, Adam and Eve lived in harmony with nature, enjoying the bountiful fruits of the garden. They were free to explore and tend to the land, and their only commandment was to abstain from eating the fruit of the Tree of Knowledge of Good and Evil. However, temptation would soon find its way into their lives in the form of a cunning serpent.The serpent, driven by its own desires, enticed Eve to eat the forbidden fruit, promising her enlightenment and wisdom.Eve, enticed by the prospect of gaining knowledge, succumbed to temptation and ate the fruit.She then shared it with Adam, who also partook, thus defying the commandment of God.Their act of disobedience had profound consequences.Suddenly, they became aware of their nakedness and experienced shame.They were banished from the Garden of Eden, condemned to a life of toil and hardship.The harmony they once enjoyed was shattered, and they were thrust into a world of pain, suffering, and mortality.The story of Adam and Eve raises numerous philosophical and theological questions.It explores the nature of human free will and the consequences of moral choices.It delves into the concept of temptation and the fragility of human nature.It also highlights the tension between human desires and divine commands, and the consequences of disobeying those commands.Furthermore, the tale of Adam and Eve can be interpreted as a metaphorical representation of the human condition.It symbolizes the loss of innocence and the entry of humanity into a world of moral complexity.It speaks to the universal human experience of grappling with desires, making choices, and facing the repercussions of those choices.Despite their disobedience, the story of Adam and Eve also contains elements of hope and redemption.God, in His mercy, provides them with garments to cover their nakedness and promises a future Savior who would ultimately reconcile humanity with the divine.This foreshadows the central message of Christianity, the belief in Jesus Christ as the redeemer who would bring salvation to all.The tale of Adam and Eve continues to captivate and resonate with people across different cultures and religions.It serves as a cautionary tale, reminding us of the consequences of yielding to temptation and the importance of moral choices.It invites us to reflect on the complexities of human nature and the pursuit of knowledge.Ultimately, it encourages us to seek redemption and strive for spiritual growth.In conclusion, the story of Adam and Eve is a profound narrative that explores the origins of humanity and grapples with fundamental questions about human nature, free will, and the consequences of choices.It serves as a powerful metaphor for the human condition and carries enduring lessons for individuals and societies alike.'''
# chunked = chunk(input_text, 'paragraphs')
# for i, chunk in enumerate(chunked):
#     print(f"Chunk {i + 1}:")
#     print(chunk)

'''
Chunk 1:
['The tale of Adam and Eve is one of the most enduring and well-known narratives in human history.']
Chunk 2:
['It is a story that explores the origins of humanity and carries profound symbolic significance. According to the biblical account, Adam and Eve were the first human beings created by God, placed in the Garden of Eden, a paradise of unimaginable beauty and perfection. In this idyllic setting, Adam and Eve lived in harmony with nature, enjoying the bountiful fruits of the garden. They were free to explore and tend to the land, and their only commandment was to abstain from eating the fruit of the Tree of Knowledge of Good and Evil. However, temptation would soon find its way into their lives in the form of a cunning serpent. The serpent, driven by its own desires, enticed Eve to eat the forbidden fruit, promising her enlightenment and wisdom. Eve, enticed by the prospect of gaining knowledge, succumbed to temptation and ate the fruit. She then shared it with Adam, who also partook, thus defying the commandment of God.'] 8
Chunk 3:
['Their act of disobedience had profound consequences. Suddenly, they became aware of their nakedness and experienced shame. They were banished from the Garden of Eden, condemned to a life of toil and hardship. The harmony they once enjoyed was shattered, and they were thrust into a world of pain, suffering, and mortality. The story of Adam and Eve raises numerous philosophical and theological questions. It explores the nature of human free will and the consequences of moral choices. It delves into the concept of temptation and the fragility of human nature. It also highlights the tension between human desires and divine commands, and the consequences of disobeying those commands. Furthermore, the tale of Adam and Eve can be interpreted as a metaphorical representation of the human condition. It symbolizes the loss of innocence and the entry of humanity into a world of moral complexity. It speaks to the universal human experience of grappling with desires, making choices, and facing the repercussions of those choices. Despite their disobedience, the story of Adam and Eve also contains elements of hope and redemption. God, in His mercy, provides them with garments to cover their nakedness and promises a future Savior who would ultimately reconcile humanity with the divine. This foreshadows the central message of Christianity, the belief in Jesus Christ as the redeemer who would bring salvation to all. The tale of Adam and Eve continues to captivate and resonate with people across different cultures and religions. It serves as a cautionary tale, reminding us of the consequences of yielding to temptation and the importance of moral choices.'] 16
Chunk 4:
['It invites us to reflect on the complexities of human nature and the pursuit of knowledge. Ultimately, it encourages us to seek redemption and strive for spiritual growth. In conclusion, the story of Adam and Eve is a profound narrative that explores the origins of humanity and grapples with fundamental questions about human nature, free will, and the consequences of choices. It serves as a powerful metaphor for the human condition and carries enduring lessons for individuals and societies alike.'] 4
'''