import re

# Проверка нумерации статей
def check_article_numbering(text):
    pattern = r'Статья (\d+)'
    numbers = [int(match) for match in re.findall(pattern, text)]
    issues = []
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i-1] + 1:
            issues.append(f"Нарушение нумерации статей: после статьи {numbers[i-1]} следует статья {numbers[i]}")
    return issues


def check_paragraphs_start(text):
    pattern = r'(?<=\n)\s*[а-я]'
    issues = []
    context_length = 30  # Количество символов для отображения до и после найденной позиции

    for match in re.finditer(pattern, text):
        start = max(match.start() - context_length, 0)
        end = min(match.end() + context_length, len(text))
        context = text[start:end].replace('\n', ' ')  # Заменяем переносы строк на пробелы для удобства чтения
        issues.append(f"Абзац начинается со строчной буквы на позиции {match.start()}. Контекст: ...{context}...")
    return issues



# Проверка формата дат
def check_date_format(text):
    pattern = r'\d{1,2} [а-я]+ \d{4} года'
    issues = []
    for match in re.finditer(pattern, text):
        if not re.fullmatch(pattern, match.group()):
            issues.append(f"Неверный формат даты: {match.group()}")
    return issues

# Проверка наличия заголовков и подзаголовков
def check_headers(text):
    patterns = {
        'раздел': r'Раздел \d+',
        'подраздел': r'Подраздел \d+',
        'параграф': r'Параграф \d+'
    }
    issues = []
    for header, pattern in patterns.items():
        if not re.search(pattern, text):
            issues.append(f"Отсутствует {header}.")
    return issues


# Объединение проверок и вывод результатов
def check_document_rules(text):
    issues = []
    issues.extend(check_article_numbering(text))
    issues.extend(check_paragraphs_start(text))
    issues.extend(check_date_format(text))
    issues.extend(check_headers(text))
    return issues

def report_issues(issues):
    if not issues:
        print("Нарушений не обнаружено.")
    else:
        print("Обнаруженные нарушения:")
        for issue in issues:
            print(issue)

# Пример использования
# Предполагается, что вы замените 'your_document.txt' на путь к вашему файлу с текстом нормативного акта
def main():
    try:
        with open('./111.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            issues = check_document_rules(text)
            report_issues(issues)
    except FileNotFoundError:
        print("Файл не найден. Убедитесь, что указали правильный путь к файлу.")

if __name__ == "__main__":
    main()
