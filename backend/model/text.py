import nltk
import re

nltk.download('punkt')

from nltk.tokenize import sent_tokenize

def chunkBySentences(text):
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

def chunkByParagraphs(text):
    '''Pattern Breakdown:
    \n{1,}: Matches one or more consecutive newline characters
    \s*: Removes whitespaces
    '''
    pattern = r"\s*\n{1,}\s*"
    paragraphs = re.split(pattern, text.strip())
    return paragraphs

def chunkFn(text, chunkOptionSent = True):
    chunkSize = 1500
    chunks = []
    currentChunk = []
    totalChars = 0
    
    # Chunk options
    if chunkOptionSent:
        chunksToProcess = chunkBySentences(text)
    else:
        chunksToProcess = chunkByParagraphs(text)
    for chunk in chunksToProcess:
        if totalChars + len(chunk) <= chunkSize:
            currentChunk.append(chunk)
            totalChars += len(chunk)
        else:
            chunks.append(currentChunk)
            currentChunk = [chunk]
            totalChars = len(chunk)
    chunks.append(currentChunk)
    print(f"Number of Chunks: {len(chunks)}")
    return chunks

input_text = '''Marilyn Monroe, born Norma Jeane Mortenson on June 1, 1926, was an iconic American actress, singer, and model. With her captivating beauty, charismatic presence, and tragic life, she remains one of the most enduring and celebrated figures in Hollywood history. Monroe's rise to stardom began in the early 1950s when she signed a contract with 20th Century Fox. Her breakthrough came with roles in films such as "Niagara" (1953) and "Gentlemen Prefer Blondes" (1953), which showcased her talent for comedic timing and her irresistible on-screen allure. Monroe's distinctive blend of innocence, sensuality, and vulnerability won the hearts of audiences worldwide. Marilyn Monroe is a good human.

Throughout her career, Monroe starred in numerous critically acclaimed films, including "Some Like It Hot" (1959), for which she received a Golden Globe award for Best Actress in a Comedy. Her performances in "The Seven Year Itch" (1955) and "Bus Stop" (1956) also garnered praise and demonstrated her range as an actress. Monroe's ability to transition seamlessly between comedic and dramatic roles solidified her status as a versatile performer.

Beyond her acting career, Monroe possessed a mesmerizing singing voice. She released several successful singles, including the iconic "Diamonds Are a Girl's Best Friend" from the film "Gentlemen Prefer Blondes." Her sultry voice and captivating stage presence made her a popular entertainer, enchanting audiences with her musical talents.

However, behind the glamour and success, Monroe faced personal struggles. She battled with mental health issues and endured a tumultuous personal life. Her marriages to Joe DiMaggio, the legendary baseball player, and playwright Arthur Miller, both ended in divorce, further adding to her emotional turmoil. Despite the challenges she faced, Monroe's legacy as an influential cultural icon endures.

Tragically, on August 5, 1962, Marilyn Monroe's life was cut short at the age of 36. Her untimely death, officially ruled as a probable suicide, sent shockwaves through the world and left an indelible mark on the entertainment industry. However, her legacy lives on, and Monroe's impact on popular culture remains undeniable.

Marilyn Monroe's enduring image as a symbol of beauty, femininity, and vulnerability continues to captivate audiences. Her timeless beauty, coupled with her undeniable talent, immortalizes her as an icon of Hollywood's golden age. Monroe's contribution to the film industry and her status as a cultural icon make her an eternal legend, forever etched in the annals of cinematic history.
'''

sentences = chunkFn(input_text, chunkOptionSent = False)
print(sentences)