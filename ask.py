import re, PyPDF2, textract, bs4, os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Open The Browser And Goes To Brainly
url = 'https://brainly.com.br'

print('Opening Chrome')
driver = webdriver.Chrome('C:/Users/saya/Documents/AskBrainly-main/chromedriver.exe')
print('Entering brainly.com')
driver.get(url)

# Save All The Answers In A Text File
def saveAnswers():
    FileName = input('Nome Do Arquivo: ')

    with open(f'MinhasRespostas\\{FileName}.txt', 'wt', encoding='utf-8') as AnswersFile:
        for index, answer in enumerate(AllAnswers):
            AnswersFile.write(f"• Questão {index + 1}\n\n{answer}\n\n\n")


# Look For Answers In Brainly
def GetAnswer(question):
    driver.switch_to.window(driver.window_handles[0])

    inputBox = driver.find_element_by_css_selector('#hero-search')
    inputBox.clear()
    driver.execute_script("arguments[0].value = arguments[1]", inputBox, question)

    searchButton = driver.find_element_by_css_selector('#__next > div > div.section--lnnYy.section--KhXv2 > div > div.sg-flex.sg-flex--full-width.sg-flex--column > div > form > div > div > button')
    ActionChains(driver).move_to_element(searchButton).key_down(Keys.CONTROL).click(searchButton).key_up(Keys.CONTROL).perform()

    driver.switch_to.window(driver.window_handles[1])

    sleep(2)

    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'lxml')

    QuestionBox = soup.select('#main-sg-layout-container > div.sg-layout__container.js-main-container > div > div.js-react-search-results > div > div > div.sg-box.sg-box--light.sg-box--padding-m.sg-box--border-color-gray-secondary-lightest.sg-box--border.LayoutBox__box--1X9rF > div > div:nth-child(2)') # body > div.js-page-wrapper > div > div.sg-layout__container.js-main-container > div > div.js-react-search-results > div.sg-box.sg-box--light.sg-box--padding-m.sg-box--border-color-gray-secondary-lightest.sg-box--border.LayoutBox__box--1X9rF > div > div:nth-child(2)
    
    EachQuestion = QuestionBox[0].find_all('div', class_='sg-flex sg-flex--full-width sg-flex--wrap sg-flex--margin-top-m') # sg-content-box sg-content-box--spaced-top-large    class="sg-flex sg-flex--full-width sg-flex--wrap sg-flex--margin-top-m"

    VerifiedAnswers = QuestionBox[0].find_all('div', class_='sg-icon sg-icon--mint sg-icon--x32 SearchItem-module__verifiedIcon--9-kRQ') #sg-icon sg-icon--mint sg-icon--x32

    print('\033[1;36mResultado Da Pesquisa\033[m\n')
    print(f'Total de Resultados Encontrados {len(EachQuestion)} ')
    print(f'Total de Resultados Verificados {len(VerifiedAnswers)}')
    print()

    link = driver.find_element_by_css_selector('#main-sg-layout-container > div.sg-layout__container.js-main-container > div > div.js-react-search-results > div > div > div.sg-box.sg-box--light.sg-box--padding-m.sg-box--border-color-gray-secondary-lightest.sg-box--border.LayoutBox__box--1X9rF > div > div:nth-child(2) > div:nth-child(1) > div') # body > div.js-page-wrapper > div > div.sg-layout__container.js-main-container > div > div.js-react-search-results > div.sg-box.sg-box--light.sg-box--padding-m.sg-box--border-color-gray-secondary-lightest.sg-box--border.LayoutBox__box--1X9rF > div > div:nth-child(2) > div:nth-child(1) > div.sg-content-box__content > a
    link.click()

    sleep(2)

    AnswerPage = driver.page_source
    AnswerSoup = bs4.BeautifulSoup(AnswerPage, 'lxml')

    AnswerElement = AnswerSoup.find('div', class_='brn-qpage-next-answer-box__content')
    try:
        answer = AnswerElement.getText().strip()
    except AttributeError:
        answer = 'NÃO ENCONTRADA'

    AllAnswers.append(answer)

    print('-'*50)
    print('Resposta Da Questão')
    print()
    print(f'\033[1;33m{answer}\033[m')
    print()

    driver.close()


# Check How Many Files Are In MeusPDFs
AllFiles = os.listdir('MeusPDFs')

PDFs = []

# Search For PDFs
for File in AllFiles:
    if File.endswith(('.pdf')):
        PDFs.append(File)

# Loop The Script
while True:
    os.system('cls')

    # Show All .pdf Files:
    print(f"\nExistem \033[1;32m{len(PDFs)}\033[m arquivos .pdf No Diretório '\033[1;31m\\MeusPDFs\033[m': \n")

    if len(PDFs) != 0:
        print('-'*69)
        print('|\033[1;34m{:^6}\033[m|\033[1;34m{:60}\033[m|'.format('id', 'Nome Do Arquivo'))
        print('-'*69)

        for index, pdf in enumerate(PDFs):
            print('|\033[1;32m{:^6}\033[m|\033[1;32m{:60}\033[m|'.format(index, pdf))

        print('-'*69)

        while True:
            pdfIndex = int(input('Index Do Arquivo A Ser Analizado: \033[1;32m'))

            if pdfIndex >= len(PDFs):
                print('\n\033[mO Index Não Corresponde A Um Arquivo No Diretório')

            else:
                break

    else:
        print("Adicione Pelo Menos Um Arquivo .pdf No Diretório '\033[1;31m\\MeusPDFs\033[m' e Reinicie O Script")
        break


    # TODO: Create A Regex Object For Different Kinds Of Questions List:
    RegexString = r"""
    # Questions That Have A Number Followed By A Dot, A Space, (With Something Inside)
    
    (

        (\d+\.\s\(.*?\).*?\.) # Provas De Vestibular
        #|
        #(\d+\.\s.*?\:) # (\d+\.\s.*\:)
        #|
        #(\d\.\d+\)\s.*?\.) # Biomateriais e Biomecânica

    )

    """

    # RegexString = r'(\d+\s\.\s\s\s\(.*?\).*?\.)'

    # QuestionRegex = re.compile(r'(\d+\s\.\s \s\(.*?\).*?\.)', re.DOTALL)
    QuestionRegex = re.compile(RegexString, re.VERBOSE | re.DOTALL) # re.VERBOSE | re.DOTALL

    # Get All Questions From a File
    print(f'\033[m\nLendo PDF: \033[1;32m{PDFs[pdfIndex]}\033[m')
    with open(f'MeusPDFs\\{PDFs[pdfIndex]}', 'rb') as pdfFile:
        ReaderObject = PyPDF2.PdfFileReader(pdfFile)
        PdfInfo = ReaderObject.documentInfo
        AllPages = []

        for pageIndex in range(ReaderObject.numPages):
            page = ReaderObject.getPage(pageIndex).extractText()
            AllPages.append(page)

        # TextFile = '\n'.join(AllPages)
        TextFile = textract.process(f'MeusPDFs\\{PDFs[pdfIndex]}').decode('utf-8')
    
        AllQuestions = QuestionRegex.findall(TextFile)


    print(len(AllQuestions))

    print('\n'*5)
    for i in AllQuestions:
        print(i[0])
    print('\n'*5)

    sleep(0.5)

    # TODO: Show PDF Info
    print('\nPDF Info:\n')

    try:
        print(f"Autor: \033[1;36m{PdfInfo['/Author']}\033[m")

    except KeyError:
        print('O Arquivo Selecionado \033[1;31mNão\033[m Registra Um Autor!')

    print()

    print(f'Páginas: \033[1;32m{len(AllPages)}\033[m')
    print(f'Questões: \033[1;32m{len(AllQuestions)}\033[m')
    print()

    sleep(1)

    print('Inicializando A Busca', end='', flush=True)
    sleep(1)
    for i in range(0, 3):

        print('.', end='', flush=True)
        sleep(0.8)

    print('\n')

    # Start The Search
    AllAnswers = []

    for index, Question in enumerate(AllQuestions):
        print('-'*50)
        print(f'\033[1;36mQuestão {index + 1}°\033[m')
        print('-'*50)
        print(f'\033[1;33m {Question[0]}\033[m')
        print('-'*50)

        GetAnswer(Question)

    saveRes = input('Gostaria de Salvar As Respostar Em Um Arquivo De Texto? (S/N) ').lower().strip()

    if saveRes == 's':
        saveAnswers()

    res = input('Deseja Continuar? (S/N) ').lower().strip()

    if res == 'n':
        break

# Close Browser
driver.switch_to.window(driver.window_handles[0])
driver.close()

