from sqlalchemy.orm import Session
import models

DEFAULT_TERMS = [
    {
        "name": "Flutter",
        "description": "Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.",
    },
    {
        "name": "Dart",
        "description": "Dart is the programming language used to write Flutter applications.",
    },
    {
        "name": "Widget",
        "description": "Widgets are the basic building blocks of a Flutter app's user interface. Each widget is an immutable declaration of part of the user interface.",
    },
    {
        "name": "StatelessWidget",
        "description": "A widget that does not require mutable state. Stateless widgets are immutable.",
    },
    {
        "name": "StatefulWidget",
        "description": "A widget that has mutable state. A stateful widget can change its appearance in response to events.",
    },
    {
        "name": "State",
        "description": "State is information that can be read synchronously when the widget is built and might change during the lifetime of the widget.",
    },
    {
        "name": "MaterialApp",
        "description": "A widget that wraps several widgets commonly required for material design applications.",
    },
    {
        "name": "Scaffold",
        "description": "Implements the basic material design visual layout structure.",
    },
    {
        "name": "BuildContext",
        "description": "A handle to the location of a widget in the widget tree.",
    },
    {
        "name": "setState",
        "description": "Notifies the framework that the internal state of this object has changed.",
    },
    {
        "name": "Pub",
        "description": "Pub is the package manager for the Dart programming language, used to manage dependencies for Flutter projects.",
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

