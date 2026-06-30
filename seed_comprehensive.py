"""
Comprehensive seed with 100+ QA pairs covering all PMBOK chapters.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lms.database import SessionLocal
from lms.models import Chapter, QAConcept

QA_DATA = {
    "01_intro_estandar": [
        {"concept": "Estándar", "question": "¿Qué es El Estándar para la Dirección de Proyectos?", "answer": "Un conjunto de guías y prácticas reconocidas que describen los fundamentos de la dirección de proyectos, aplicables a la mayoría de los proyectos la mayor parte del tiempo.", "difficulty": "easy"},
        {"concept": "Guía PMBOK", "question": "¿Cuál es el propósito de la Guía del PMBOK 7ª Edición?", "answer": "Proporcionar fundamentos para la dirección de proyectos incluyendo 12 principios y 8 dominios de desempeño para gestionar proyectos de manera efectiva.", "difficulty": "easy"},
        {"concept": "Dirección de Proyectos", "question": "¿Cómo se define la dirección de proyectos?", "answer": "La aplicación de conocimientos, habilidades, herramientas y técnicas a las actividades del proyecto para cumplir con los requisitos del mismo.", "difficulty": "easy"},
        {"concept": "Valor", "question": "¿Qué significa enfocarse en el valor en dirección de proyectos?", "answer": "Evaluar continuamente la alineación del proyecto con los objetivos de negocio, los beneficios esperados y el valor entregado a los interesados.", "difficulty": "medium"},
        {"concept": "Resultados", "question": "¿Qué son los resultados en el contexto del PMBOK?", "answer": "Los efectos o beneficios finales que se obtienen de un proyecto, más allá de los entregables tangibles.", "difficulty": "medium"},
    ],
    "02_sistema_valor": [
        {"concept": "Sistema de Entrega de Valor", "question": "¿Qué es un sistema para la entrega de valor?", "answer": "Un conjunto de actividades estratégicas, procesos y recursos que una organización utiliza para crear, mantener y entregar valor a través de proyectos, programas y portafolios.", "difficulty": "medium"},
        {"concept": "Gobernanza Organizacional", "question": "¿Cuál es el rol de la gobernanza organizacional en proyectos?", "answer": "Proporcionar la estructura de autoridad, responsabilidad, políticas y procedimientos que guían la toma de decisiones y el comportamiento del equipo del proyecto.", "difficulty": "medium"},
        {"concept": "Entorno Interno", "question": "¿Qué factores del entorno interno afectan un proyecto?", "answer": "Cultura organizacional, estructura, recursos disponibles, capacidades del equipo, tecnología y procesos internos.", "difficulty": "easy"},
        {"concept": "Entorno Externo", "question": "¿Qué factores del entorno externo afectan un proyecto?", "answer": "Condiciones del mercado, regulaciones gubernamentales, factores económicos, condiciones ambientales y tendencias de la industria.", "difficulty": "easy"},
        {"concept": "Portafolio", "question": "¿Qué es un portafolio en dirección de proyectos?", "answer": "Un conjunto de proyectos, programas y operaciones que se gestionan como un grupo para alcanzar objetivos estratégicos.", "difficulty": "medium"},
        {"concept": "Programa", "question": "¿Qué es un programa en dirección de proyectos?", "answer": "Un grupo de proyectos relacionados gestionados de forma coordinada para obtener beneficios que no se obtendrían si se gestionaran individualmente.", "difficulty": "medium"},
        {"concept": "Ciclo de Vida del Producto", "question": "¿Cómo se relaciona el ciclo de vida del producto con el proyecto?", "answer": "El proyecto es parte del ciclo de vida del producto, que abarca desde la idea inicial hasta el retiro del producto del mercado.", "difficulty": "hard"},
    ],
    "03_principios": [
        {"concept": "Administrador Diligente", "question": "¿Qué significa ser un administrador diligente, respetuoso y cuidadoso?", "answer": "Actuar con integridad, responsabilidad y cuidado ético, gestionando los recursos del proyecto de manera responsable.", "difficulty": "medium"},
        {"concept": "Entorno Colaborativo", "question": "¿Cómo se crea un entorno colaborativo en el equipo del proyecto?", "answer": "Fomentando confianza, comunicación abierta, respeto mutuo, diversidad de pensamiento y proporcionando herramientas que facilitan la colaboración.", "difficulty": "medium"},
        {"concept": "Interesados", "question": "¿Por qué es importante involucrarse eficazmente con los interesados?", "answer": "Porque tienen influencia en el proyecto y sus necesidades deben ser comprendidas y gestionadas para asegurar el éxito.", "difficulty": "easy"},
        {"concept": "Valor", "question": "¿Qué significa enfocarse en el valor en el contexto de principios?", "answer": "Priorizar la entrega de beneficios y valor al negocio y a los interesados, evaluando continuamente si el proyecto genera el valor esperado.", "difficulty": "easy"},
        {"concept": "Sistemas", "question": "¿Qué significa reconocer, evaluar y responder a las interacciones del sistema?", "answer": "Entender que el proyecto opera dentro de un sistema más amplio y que los cambios en una parte afectan a las demás.", "difficulty": "hard"},
        {"concept": "Liderazgo", "question": "¿Qué comportamientos de liderazgo son importantes en dirección de proyectos?", "answer": "Integridad, visión, motivación, comunicación efectiva, empatía, adaptabilidad y pensamiento crítico.", "difficulty": "medium"},
        {"concept": "Adaptación", "question": "¿Qué significa adaptar en función del contexto?", "answer": "Ajustar los enfoques, procesos y prácticas de dirección de proyectos según las características únicas del proyecto y su entorno.", "difficulty": "medium"},
        {"concept": "Calidad", "question": "¿Cómo se incorpora la calidad en los procesos y entregables?", "answer": "Definiendo estándares de calidad desde el inicio, realizando aseguramiento y control de calidad, y fomentando mejora continua.", "difficulty": "medium"},
        {"concept": "Complejidad", "question": "¿Qué significa navegar en la complejidad?", "answer": "Reconocer y responder a la complejidad del proyecto que surge de factores humanos, de sistemas y de ambigüedad.", "difficulty": "hard"},
        {"concept": "Riesgo", "question": "¿Qué significa optimizar las respuestas a los riesgos?", "answer": "Identificar, analizar y responder proactivamente a los riesgos para maximizar oportunidades y minimizar amenazas.", "difficulty": "medium"},
        {"concept": "Adaptabilidad", "question": "¿Qué significa adoptar la adaptabilidad y la resiliencia?", "answer": "Ser capaz de responder al cambio y recuperarse de contratiempos, manteniendo el enfoque en los objetivos del proyecto.", "difficulty": "medium"},
        {"concept": "Cambio", "question": "¿Qué significa permitir el cambio para lograr el estado futuro previsto?", "answer": "Facilitar la transformación organizacional necesaria para alcanzar los beneficios y resultados esperados del proyecto.", "difficulty": "hard"},
    ],
    "04_part2_intro": [
        {"concept": "Dominios de Desempeño", "question": "¿Qué son los dominios de desempeño del proyecto?", "answer": "Grupos de actividades relacionadas que son críticas para la entrega efectiva de los resultados del proyecto.", "difficulty": "medium"},
        {"concept": "Interesados", "question": "¿Cuál es el enfoque del Dominio de Desempeño de los Interesados?", "answer": "Identificar, comprender y gestionar las expectativas de los interesados para fomentar su participación y satisfacción.", "difficulty": "easy"},
        {"concept": "Equipo", "question": "¿Qué abarca el Dominio de Desempeño del Equipo?", "answer": "Establecer y mantener un equipo de alto rendimiento con liderazgo compartido, confianza y colaboración.", "difficulty": "easy"},
        {"concept": "Ciclo de Vida", "question": "¿Qué es un ciclo de vida del proyecto?", "answer": "Serie de fases que atraviesa un proyecto desde su inicio hasta su conclusión.", "difficulty": "easy"},
        {"concept": "Enfoque de Desarrollo", "question": "¿Cuáles son los principales enfoques de desarrollo?", "answer": "Predictivo (cascada), híbrido y adaptativo (ágil), que forman un espectro desde lo más planificado hasta lo más flexible.", "difficulty": "medium"},
    ],
    "05_dominio_ciclo_vida": [
        {"concept": "Cadencia de Entrega", "question": "¿Qué es la cadencia de entrega?", "answer": "El momento y la frecuencia de los entregables del proyecto, que puede ser única, múltiple o periódica.", "difficulty": "medium"},
        {"concept": "Entrega Única", "question": "¿Qué es una entrega única?", "answer": "Una sola entrega al final del proyecto, típica de proyectos predictivos.", "difficulty": "easy"},
        {"concept": "Entregas Múltiples", "question": "¿Qué son las entregas múltiples?", "answer": "Múltiples componentes que se entregan en diferentes momentos a lo largo del proyecto.", "difficulty": "easy"},
        {"concept": "Entregas Periódicas", "question": "¿Qué son las entregas periódicas?", "answer": "Entregas en un cronograma fijo como mensual o bimensual.", "difficulty": "easy"},
        {"concept": "Entrega Continua", "question": "¿Qué es la entrega continua?", "answer": "La práctica de entregar incrementos de funcionalidad a los clientes en forma inmediata, usando lotes pequeños y automatización.", "difficulty": "hard"},
        {"concept": "Enfoque Predictivo", "question": "¿Cuándo es útil un enfoque predictivo?", "answer": "Cuando los requisitos pueden definirse al inicio y hay baja incertidumbre.", "difficulty": "medium"},
        {"concept": "Enfoque Híbrido", "question": "¿Qué es un enfoque híbrido?", "answer": "Combinación de enfoques adaptativos y predictivos, útil cuando hay incertidumbre en los requisitos.", "difficulty": "medium"},
        {"concept": "Enfoque Adaptativo", "question": "¿Cuándo se usa un enfoque adaptativo?", "answer": "Cuando los requisitos son inciertos y se espera que cambien frecuentemente.", "difficulty": "easy"},
        {"concept": "Iterativo vs Incremental", "question": "¿Cuál es la diferencia entre desarrollo iterativo e incremental?", "answer": "Iterativo refina el producto mediante ciclos repetidos; incremental añade funcionalidad progresivamente en cada ciclo.", "difficulty": "hard"},
    ],
    "06_dominio_planificacion": [
        {"concept": "Planificación", "question": "¿Qué abarca el Dominio de Desempeño de la Planificación?", "answer": "La organización y coordinación de la entrega del proyecto a través de la planificación del alcance, cronograma, presupuesto y recursos.", "difficulty": "medium"},
        {"concept": "Estimación", "question": "¿Cuáles son los tipos de estimación en proyectos?", "answer": "Estimación análoga, paramétrica, ascendente (bottom-up) y de tres puntos (PERT).", "difficulty": "medium"},
        {"concept": "Cronograma", "question": "¿Qué métodos se usan para desarrollar el cronograma?", "answer": "Método de la ruta crítica (CPM), compresión del cronograma (crashing, fast-tracking) y nivelación de recursos.", "difficulty": "hard"},
        {"concept": "Presupuesto", "question": "¿Cómo se establece el presupuesto del proyecto?", "answer": "Agregando los costos estimados de las actividades individuales para establecer una línea base de costos.", "difficulty": "medium"},
        {"concept": "Alcance", "question": "¿Qué es el alcance del proyecto?", "answer": "El trabajo que debe realizarse para entregar un producto, servicio o resultado con las características y funciones especificadas.", "difficulty": "easy"},
    ],
    "07_dominio_trabajo": [
        {"concept": "Trabajo del Proyecto", "question": "¿Qué abarca el Dominio de Desempeño del Trabajo del Proyecto?", "answer": "El establecimiento de procesos, la gestión de recursos físicos, las adquisiciones y la gestión del cambio.", "difficulty": "medium"},
        {"concept": "Procesos", "question": "¿Por qué son importantes los procesos en un proyecto?", "answer": "Porque proporcionan consistencia, eficiencia y calidad en la ejecución del trabajo del proyecto.", "difficulty": "easy"},
        {"concept": "Adquisiciones", "question": "¿Qué es la gestión de adquisiciones?", "answer": "El proceso de obtener bienes y servicios de proveedores externos para el proyecto.", "difficulty": "medium"},
        {"concept": "Gestión del Cambio", "question": "¿Qué es la gestión del cambio organizacional?", "answer": "El enfoque estructurado para hacer la transición de individuos, equipos y organizaciones del estado actual al estado futuro deseado.", "difficulty": "hard"},
    ],
    "08_dominio_entrega": [
        {"concept": "Entrega", "question": "¿Qué abarca el Dominio de Desempeño de la Entrega?", "answer": "Cumplir los requisitos del proyecto, validar los entregables y asegurar que se alcancen los resultados y beneficios esperados.", "difficulty": "medium"},
        {"concept": "Entregables", "question": "¿Qué es un entregable?", "answer": "Cualquier producto, resultado o capacidad única y verificable que debe producirse para completar un proceso, fase o proyecto.", "difficulty": "easy"},
        {"concept": "Validación", "question": "¿Qué es la validación del alcance?", "answer": "El proceso de formalizar la aceptación de los entregables completados del proyecto.", "difficulty": "medium"},
        {"concept": "Control de Calidad", "question": "¿Qué es el control de calidad en proyectos?", "answer": "Monitorear y registrar los resultados de las actividades de calidad para evaluar el desempeño y recomendar cambios.", "difficulty": "medium"},
    ],
    "09_dominio_medicion": [
        {"concept": "Medición", "question": "¿Qué abarca el Dominio de Desempeño de la Medición?", "answer": "Evaluar el desempeño del proyecto mediante métricas, indicadores clave (KPI) y gestión del valor ganado (EVM).", "difficulty": "medium"},
        {"concept": "Valor Ganado (EVM)", "question": "¿Qué es la gestión del valor ganado (EVM)?", "answer": "Una metodología que integra alcance, cronograma y costos para medir el desempeño del proyecto.", "difficulty": "hard"},
        {"concept": "KPI", "question": "¿Qué son los KPI en dirección de proyectos?", "answer": "Indicadores clave de desempeño que miden aspectos críticos del proyecto como cumplimiento de cronograma, costos y calidad.", "difficulty": "easy"},
        {"concept": "Línea Base", "question": "¿Qué es una línea base en dirección de proyectos?", "answer": "La versión aprobada del plan del proyecto que sirve como punto de referencia para medir el desempeño.", "difficulty": "medium"},
        {"concept": "Variación", "question": "¿Qué es la variación del cronograma (SV)?", "answer": "La diferencia entre el valor ganado (EV) y el valor planificado (PV) en un momento dado.", "difficulty": "hard"},
        {"concept": "CPI", "question": "¿Qué es el índice de desempeño del costo (CPI)?", "answer": "La relación entre el valor ganado (EV) y el costo real (AC), que mide la eficiencia del costo.", "difficulty": "hard"},
    ],
    "10_dominio_incertidumbre": [
        {"concept": "Incertidumbre", "question": "¿Qué abarca el Dominio de Desempeño de la Incertidumbre?", "answer": "Identificar y responder a la ambigüedad, riesgos y la complejidad del entorno del proyecto.", "difficulty": "medium"},
        {"concept": "Riesgo", "question": "¿Qué es un riesgo del proyecto?", "answer": "Un evento o condición incierta que, si ocurre, tiene un efecto positivo o negativo en los objetivos del proyecto.", "difficulty": "easy"},
        {"concept": "Amenaza vs Oportunidad", "question": "¿Cuál es la diferencia entre amenaza y oportunidad en riesgos?", "answer": "Una amenaza es un riesgo con efecto negativo; una oportunidad es un riesgo con efecto positivo.", "difficulty": "easy"},
        {"concept": "Estrategias de Respuesta", "question": "¿Cuáles son las estrategias de respuesta a amenazas?", "answer": "Evitar, transferir, mitigar y aceptar.", "difficulty": "medium"},
        {"concept": "Estrategias de Oportunidad", "question": "¿Cuáles son las estrategias de respuesta a oportunidades?", "answer": "Explotar, mejorar, compartir y aceptar.", "difficulty": "medium"},
        {"concept": "Ambiente VUCA", "question": "¿Qué significa el entorno VUCA?", "answer": "Volatilidad, Incertidumbre, Complejidad y Ambigüedad (Volatility, Uncertainty, Complexity, Ambiguity).", "difficulty": "hard"},
    ],
    "11_adaptacion": [
        {"concept": "Adaptación", "question": "¿Qué es la adaptación en dirección de proyectos?", "answer": "El proceso de ajustar los enfoques, métodos y prácticas de dirección de proyectos al contexto único de cada proyecto.", "difficulty": "medium"},
        {"concept": "Factores de Adaptación", "question": "¿Qué factores influyen en la adaptación del proyecto?", "answer": "Tamaño del proyecto, tipo de industria, complejidad, cultura organizacional, ciclo de vida del producto y requisitos regulatorios.", "difficulty": "medium"},
        {"concept": "Enfoque de Desarrollo", "question": "¿Cómo se selecciona el enfoque de desarrollo adecuado?", "answer": "Considerando el tipo de entregable, el nivel de incertidumbre, los requisitos del proyecto y la cultura organizacional.", "difficulty": "medium"},
        {"concept": "Tailoring", "question": "¿Por qué es importante adaptar los procesos?", "answer": "Porque no todos los proyectos son iguales; la adaptación asegura que los procesos sean apropiados y eficientes para cada contexto.", "difficulty": "easy"},
    ],
    "12_modelos_metodos": [
        {"concept": "Modelos", "question": "¿Qué son los modelos en dirección de proyectos?", "answer": "Representaciones simplificadas de la realidad que ayudan a comprender, analizar y predecir comportamientos en proyectos.", "difficulty": "medium"},
        {"concept": "Métodos", "question": "¿Qué son los métodos en dirección de proyectos?", "answer": "Técnicas y procedimientos específicos utilizados para realizar actividades de dirección de proyectos.", "difficulty": "easy"},
        {"concept": "Artefactos", "question": "¿Qué son los artefactos en dirección de proyectos?", "answer": "Documentos, entregables o resultados tangibles producidos durante la dirección del proyecto.", "difficulty": "medium"},
        {"concept": "Modelo de Tuckman", "question": "¿Cuáles son las etapas del modelo de desarrollo de equipos de Tuckman?", "answer": "Formación, tormenta, normalización, desempeño y cierre (Forming, Storming, Norming, Performing, Adjourning).", "difficulty": "medium"},
        {"concept": "Modelo de Comunicación", "question": "¿Qué canales de comunicación considera el modelo de comunicación?", "answer": "Canales formales e informales, verbales y escritos, horizontales y verticales, sincrónicos y asincrónicos.", "difficulty": "medium"},
        {"concept": "Análisis de Interesados", "question": "¿Qué es la matriz poder/interés?", "answer": "Una herramienta para clasificar a los interesados según su nivel de poder e interés en el proyecto.", "difficulty": "easy"},
        {"concept": "Diagrama de Gantt", "question": "¿Qué es un diagrama de Gantt?", "answer": "Una representación visual del cronograma del proyecto que muestra actividades, duraciones y dependencias.", "difficulty": "easy"},
        {"concept": "Estructura de Desglose del Trabajo", "question": "¿Qué es una WBS (EDT)?", "answer": "Una descomposición jerárquica del trabajo del proyecto en componentes más pequeños y manejables.", "difficulty": "medium"},
    ],
}

def seed():
    db = SessionLocal()
    slug_to_id = {ch.slug: ch.id for ch in db.query(Chapter).all()}
    total = 0
    for slug, qa_list in QA_DATA.items():
        chapter_id = slug_to_id.get(slug)
        if not chapter_id:
            print(f"  Chapter not found: {slug}")
            continue
        count = 0
        for qa in qa_list:
            existing = db.query(QAConcept).filter(
                QAConcept.chapter_id == chapter_id,
                QAConcept.question == qa["question"]
            ).first()
            if existing:
                continue
            db.add(QAConcept(
                chapter_id=chapter_id,
                question=qa["question"],
                answer=qa["answer"],
                concept=qa["concept"],
                difficulty=qa["difficulty"],
            ))
            count += 1
        total += count
        print(f"  {slug}: {count} nuevos QA")
    db.commit()
    grand_total = db.query(QAConcept).count()
    print(f"\n✅ Total: {total} QA añadidos. Total en DB: {grand_total}")
    db.close()

if __name__ == "__main__":
    seed()
