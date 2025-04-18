# ML System Design Document for UniRec

__version__: 0.1.1

## Описание

__UniRec__ - смарт-платформа, предназначенная для предоставления персонализированных рекомендаций и анализа для бизнеса и частных лиц.  
Наша платформа использует передовые технологии обработки естественного языка и машинного обучения для сбора и анализа данных из различных источников, включая интернет-страницы, социальные сети и другие онлайн-платформы.  
Независимо от того, хотите ли вы узнать больше о своих конкурентах, найти альтернативы для определенных мест или улучшить свой бизнес, UniRec предлагает всеобъемлющий набор инструментов для удовлетворения ваших потребностей.  

## Проблематика

В современном мире, перенасыщенном информацией, владельцам бизнеса и частным лицам все сложнее ориентироваться в конкурентной среде и находить оптимальные решения. Анализ рынка, конкурентов, выявление трендов и понимание аудитории требует значительных временных и ресурсных затрат. UniRec берет на себя эту задачу, предоставляя пользователям комплексный анализ в автоматизированном режиме.

 ## Основные функции проекта

__Анализ запросов пользователей__:  
UniRec принимает запросы пользователей вместе со ссылками на платформы, которые их интересуют. UniRec обрабатывает эти ссылки, извлекая текстовую информацию и выделяя ключевые теги и темы.

__Сбор данных__:  
После анализа запроса UniRec переходит по указанным ссылкам и собирает подробную информацию, используя адаптеры для популярных социальных сетей и платформ, таких как VK, Instagram, Telegram и YouTube.

__Генерация саммари__:  
UniRec предоставляет пользователям краткое изложение (саммари) по месту или организации, указанной в запросе. Это помогает пользователям быстро получить представление о предмете их интереса.

__Анализ и рекомендации__:  
Платформа проводит тщательный анализ собранных данных и предоставляет ценные рекомендации.  
Например, если пользователь хочет улучшить свой бизнес, UniRec может предложить идеи по маркетингу, привлечению клиентов или управлению репутацией. В случае с поиском альтернативных ресторанов, платформа может выделить ключевые характеристики, которые пользователю не понравились, и предложить заведения с улучшенными параметрами.

__Поиск конкурентов и аналогов__:  
UniRec находит и представляет саммари о конкурентах или аналогичных местах вместе со ссылками на них. Это позволяет пользователям легко сравнивать и выбирать среди различных вариантов.

__Анализ аудитории__:  
Одна из ключевых особенностей UniRec - это возможность создавать профили целевой аудитории. Платформа анализирует посетителей определенных мест или подписчиков блогеров, выявляя демографические данные, интересы и предпочтения. Это дает пользователям глубокое понимание своей аудитории и помогает в принятии решений, связанных с бизнесом или маркетингом.

## Ключевые преимущества UniRec

__Экономия времени и ресурсов__: автоматизация процесса сбора и анализа информации.  
__Объективность и точность__: использование передовых алгоритмов и машинного обучения для обеспечения высокой точности анализа.  
__Персонализированные рекомендации__: анализ данных на основе конкретных потребностей и задач пользователя.  
__Комплексный подход__: учет информации из различных источников, включая веб-сайты, социальные сети и видеохостинги.
__Понимание аудитории__: глубокий анализ целевой аудитории, позволяющий оптимизировать маркетинговые стратегии и улучшить качество обслуживания.
__Масштабируемость__: платформа легко адаптируется к различным отраслям и типам бизнеса.

## Примеры использования UniRec

__Микрофинансовые организации__: анализ конкурентов, выявление лучших практик, оптимизация условий кредитования.  
__Владельцы ресторанов__: анализ конкурентов, оценка качества обслуживания, выявление трендов в кулинарии.  
__Блогеры и инфлюенсеры__: анализ целевой аудитории, оптимизация контента, привлечение новых подписчиков.
__Маркетинговые агентства__: анализ рынка, определение целевой аудитории, разработка эффективных маркетинговых стратегий.  

## Планы развития:

- Расширение списка поддерживаемых платформ и источников данных.  
- Интеграция с CRM-системами и другими бизнес-инструментами.  
- Разработка API для интеграции с другими приложениями.  
- Разработка мобильного приложения.  
- Добавление функции прогнозирования трендов и предсказания поведения аудитории.  

# Архитектура проекта

UniRec реализована как микросервисная архитектура, что обеспечит масштабируемость, гибкость и независимость компонентов.  

Основные компоненты:  

Frontend (JS) - интерактивный веб-интерфейс для взаимодействия пользователей с платформой.  
Backend (Python/FastAPI) - API для обработки запросов, управления данными и интеграции с другими компонентами.  
Data Pipeline (Airflow/Kafka) - автоматизированный процесс сбора, обработки и хранения данных.  
Storage (S3/ClickHouse) - хранение данных, включая текст, теги и результаты анализа.  
ML Component (MLFlow/LLM) - компонент машинного обучения для анализа текста, выделения тегов, анализа аудитории и генерации рекомендаций.  

## Компоненты и технологии

### Frontend (JS)

__Технологии__: JavaScript, HTML, CSS.  

Функциональность:  
- интерфейс для ввода запросов и добавления ссылок;  
- отображение результатов анализа и рекомендаций;  
- визуализация данных (графики, диаграммы);  
- управление пользователями и профилями.

### Backend (Python/FastAPI)

__Технологии__: Python, FastAPI, Uvicorn (ASGI сервер), Pydantic (для валидации данных).

Функциональность:  
- обработка запросов от Frontend;  
- управление данными и взаимодействие с другими компонентами;  
- создание и управление API endpoints;  
- аутентификация и авторизация пользователей;  
- логирование и мониторинг.

### Data Pipeline (Airflow/Kafka)

__Airflow__: оркестратор задач, ответственный за планирование и выполнение процесса сбора и обработки данных.  
Задачи:  
- извлечение данных из веб-страниц (web scraping) с использованием библиотек типа Scrapy.  
- предварительная обработка данных (очистка текста, удаление HTML-тегов, нормализация).  
- отправка данных в Kafka.  

__Kafka__: распределенная платформа потоковой передачи данных, используемая для передачи данных между компонентами.  
Применение: передача собранных данных из Airflow в ML-компонент и Storage.

### Storage

__ClickHouse__: высокопроизводительная колоночная СУБД, идеально подходящая для хранения и анализа больших объемов текстовых данных и метаданных.

Применение: хранение собранных текстов, выделенных тегов, результатов анализа и профилей аудитории.  

Схема данных:  
- web_pages (page_id, url, content, date_collected)  
- tags (tag_id, tag_name)  
- page_tags (page_id, tag_id)  
- audience_profiles (profile_id, page_id, demographic_data, interests)  

__S3 (или альтернатива - MinIO)__: может использоваться для хранения исходных HTML-страниц и других файлов. MinIO удобен для локальной разработки.

### ML Component

__MLFlow__: платформа для управления жизненным циклом машинного обучения (экспериментирование, отслеживание результатов, развертывание моделей).  
__LLM (Large Language Model)__: модели, Gemma или Llama 3.  

Задачи:  
- выделение ключевых сущностей (NER - Named Entity Recognition): определение и классификация ключевых сущностей в тексте (например, названия организаций, продуктов, локаций).  
- анализ тональности (Sentiment Analysis): определение эмоциональной окраски текста.  
- автоматическое тегирование (Automatic Tagging): назначение релевантных тегов тексту на основе его содержания.  
- генерация саммари (Summarization): создание краткого обзора текста.  
- анализ аудитории (Audience Analysis): на основе текста (например, комментариев, отзывов) определение характеристик аудитории.  

__Библиотеки__: Transformers (Hugging Face), spaCy, scikit-learn.  
__Модель__: Fine-tuning pre-trained LLM будем производить на собственных данных.  

Workflow:  
Данные из Kafka поступают в ML-компонент.  
LLM (или другие модели машинного обучения) анализирует текст.  
Результаты анализа (теги, саммари, профили аудитории) сохраняются в ClickHouse.  

### Инфраструктура и развертывание

__Docker__: использование Docker для контейнеризации всех компонентов системы, что упрощает развертывание и обеспечивает переносимость.  
__Kubernetes (k8s)__: оркестратор контейнеров, который управляет развертыванием, масштабированием и обновлением компонентов системы.  
__CI/CD__: для автоматического развертывания обновлений.  

### Поток данных

1) Пользователь отправляет запрос через Frontend.  
2) Запрос поступает в API Gateway.  
3) API Gateway аутентифицирует и авторизует пользователя.  
4) API Gateway перенаправляет запрос в соответствующий обработчик.  
5) Обработчик запускает задачи Airflow.  
6) Airflow запускает задачи Web Scraping и Data Preprocessing.  
7) Airflow передает данные в Kafka.  
8) Kafka передает данные в ClickHouse и LLM.  
9) LLM анализирует данные и сохраняет результаты в ClickHouse.  
10) ClickHouse предоставляет данные для Frontend.  

