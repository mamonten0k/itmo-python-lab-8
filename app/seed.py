from sqlalchemy.orm import Session
import models

DEFAULT_TERMS = [
    {
        "name": "Flutter",
        "description": "Флаттер это UI-инструментарий от Google для разработки нативно компилируемых приложений для мобильных платформ, веба и настольных устройств на основе одного исходного кода.",
    },
    {
        "name": "Dart",
        "description": "Dart — это язык программирования, используемый для создания приложений на Flutter. Dart ориентирован на разработку интерфейсов, имеет строгую типизацию и поддерживает как JIT, так и AOT-компиляцию.",
    },
    {
        "name": "Widget",
        "description": "Виджеты — это базовые строительные блоки пользовательского интерфейса приложения Flutter. Каждый виджет является неизменяемым описанием части интерфейса и определяет, как отображается или взаимодействует компонент.",
    },
    {
        "name": "StatelessWidget",
        "description": "Виджет, который не имеет изменяемого состояния. Такие виджеты остаются неизменными на протяжении всего времени существования. Они используются для отображения статической информации.",
    },
    {
        "name": "StatefulWidget",
        "description": "Виджет, который имеет изменяемое состояние. Такие виджеты могут обновлять свое представление при изменении состояния и реагировать на события в приложении.",
    },
    {
        "name": "State",
        "description": "Состояние — это информация, которая может быть считана синхронно во время построения виджета и может изменяться в течение его жизненного цикла. State управляет тем, как объект реагирует на изменения данных.",
    },
    {
        "name": "MaterialApp",
        "description": "Виджет, который оборачивает несколько других виджетов, необходимых для создания приложений на основе Material Design. Он предоставляет основные функции навигации, темы и локализации.",
    },
    {
        "name": "Scaffold",
        "description": "Scaffold предоставляет базовую структуру визуального интерфейса Material Design, включая AppBar, Drawer и FAB (плавающая кнопка действия).",
    },
    {
        "name": "BuildContext",
        "description": "Ссылка на расположение виджета в дереве виджетов. Он используется для предоставления информации о структуре интерфейса и обращения к родительским или дочерним виджетам.",
    },
    {
        "name": "setState",
        "description": "Метод уведомляет фреймворк Flutter о том, что внутреннее состояние объекта изменилось. Это вызывает повторное построение виджета, чтобы отобразить изменения.",
    },
    {
        "name": "Pub",
        "description": "Менеджер пакетов для языка программирования Dart. Он используется для управления зависимостями в проектах Flutter и Dart, включая установку сторонних библиотек.",
    },
]

DEFAULT_RELATIONSHIPS = [
    # Flutter and Dart
    {"term_1_name": "Flutter", "term_2_name": "Dart", "relation_type": "uses"},
    
    # Widgets and Flutter
    {"term_1_name": "Widget", "term_2_name": "Flutter", "relation_type": "is a building block of"},
    
    # Types of Widgets
    {"term_1_name": "StatelessWidget", "term_2_name": "Widget", "relation_type": "is a type of"},
    {"term_1_name": "StatefulWidget", "term_2_name": "Widget", "relation_type": "is a type of"},
    {"term_1_name": "MaterialApp", "term_2_name": "Widget", "relation_type": "is a type of"},
    {"term_1_name": "Scaffold", "term_2_name": "Widget", "relation_type": "is a type of"},
    
    # State and Widgets
    {"term_1_name": "StatefulWidget", "term_2_name": "State", "relation_type": "manages"},
    {"term_1_name": "StatelessWidget", "term_2_name": "State", "relation_type": "does not have"},
    {"term_1_name": "State", "term_2_name": "Widget", "relation_type": "affects"},
    
    # setState and StatefulWidget
    {"term_1_name": "StatefulWidget", "term_2_name": "setState", "relation_type": "uses"},
    
    # BuildContext and Widgets
    {"term_1_name": "BuildContext", "term_2_name": "Widget", "relation_type": "provides location for"},
    
    # Pub and Dart
    {"term_1_name": "Pub", "term_2_name": "Dart", "relation_type": "manages packages for"},
]

def seed_data(db: Session):
    term_name_to_id = {}

    # Add Terms
    for term in DEFAULT_TERMS:
        existing_term = db.query(models.Term).filter(models.Term.name == term["name"]).first()
        if not existing_term:
            new_term = models.Term(**term)
            db.add(new_term)
            db.commit()
            db.refresh(new_term)
            term_name_to_id[term['name']] = new_term.id
        else:
            term_name_to_id[term['name']] = existing_term.id

    # Add Relationships
    for rel in DEFAULT_RELATIONSHIPS:
        term_1_id = term_name_to_id.get(rel['term_1_name'])
        term_2_id = term_name_to_id.get(rel['term_2_name'])
        if term_1_id and term_2_id:
            existing_rel = db.query(models.Relationship).filter_by(
                term_1_id=term_1_id,
                term_2_id=term_2_id,
                relation_type=rel['relation_type']
            ).first()
            if not existing_rel:
                new_rel = models.Relationship(
                    term_1_id=term_1_id,
                    term_2_id=term_2_id,
                    relation_type=rel['relation_type']
                )
                db.add(new_rel)

    db.commit()

