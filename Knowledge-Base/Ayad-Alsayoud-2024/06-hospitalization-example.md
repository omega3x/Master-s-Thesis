# Пример Hospitalization (из GitHub авторов)

Данные ниже взяты из официального репозитория статьи, **не выдуманы**.

**Источник:** `Literature/Ayad2024-BusinessModelPrompt/BusinessModelPrompt/`

---

## Файлы примера

| Файл | Назначение |
|------|------------|
| `Medical2.xpdl` | Процесс госпитализации в XPDL 2.2 |
| `Hospitalization_BP.bpm` | Модель Bizagi |
| `Parsing_xml.py` | Извлечение в CSV |
| `The_extracted_Lanes.csv` | Дорожки |
| `The_extracted_Activities.csv` | Активности + координаты |
| `The_extracted_Lanes_Activity.csv` | Сопоставление lane → activities |

---

## Дорожки (Lanes)

| Lane | Роль |
|------|------|
| Patient | Пациент |
| Secretary | Секретарь / регистратура |
| Doctor | Врач |
| Nurse | Медсестра |

---

## Активности по дорожкам

### Patient
- Enter the registration form

### Secretary
- Welcome the patient
- Refer the patient to the medical department

### Doctor
- Consult the patient
- inquire symptoms
- Order tests

### Nurse
- take the lab results
- Inform the results to the ward team
- Observe the symtoms during the patient's stay

*(В CSV есть также unnamed activities — события/шлюзы без Name в XPDL.)*

---

## Что LLM мог бы предложить (иллюстрация метода)

Это **не из статьи дословно**, а пример логики semantic enhancement:

| Тип | Возможное предложение | Роль |
|-----|----------------------|------|
| Activity | Verify insurance coverage | Secretary |
| Activity | Assign hospital room | Nurse |
| Activity | Discharge planning | Doctor |
| Artifact | Insurance card | Registration |
| Artifact | Lab results report | Nurse → Doctor |
| Artifact | Discharge summary | Doctor |

Моделировщик выбирает релевантные → модель становится семантически полнее.

---

## Как воспроизвести парсинг

```bash
cd Literature/Ayad2024-BusinessModelPrompt/BusinessModelPrompt
python Parsing_xml.py
```

Скрипт перезапишет CSV в той же папке.

---

## Связь с Bizagi

Преподаватель просила **XPDL** для симуляции в Bizagi — именно этот формат используют Ayad & Alsayoud.

Наш `Medical2.xpdl` (у авторов) и наш `XPDL/Output/testx.xpdl` — один класс артефактов.
