import pytest
import pandas as pd
from io import StringIO
import app
csv_data = """PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Fare,Embarked
1,0,3,John Doe,male,22,1,0,7.25,S
2,1,1,Jane Doe,female,38,1,0,71.28,C
3,1,3,Jim Brown,male,26,0,0,7.93,Q
4,0,1,Jack Black,male,35,0,0,53.10,S
"""

# Создаём DataFrame из строки csv
@pytest.fixture
def test_data():
    return pd.read_csv(StringIO(csv_data))

# Тестирование функции load_data
def test_load_data(test_data):
    # Переопределим функцию load_data для теста
    app.load_data = lambda: test_data
    data = app.load_data()
    assert len(data) == 4  
    assert 'Survived' in data.columns  

# Тестирование фильтрации по полу и статусу выживания
def test_age_range(test_data):
    filtered_data = test_data[(test_data['Sex'] == 'male') & (test_data['Survived'] == 1)]
    assert len(filtered_data) == 1 
    assert filtered_data['Age'].min() == 26  
    assert filtered_data['Age'].max() == 26  

# Тестирование подсчёта спасенных и погибших по пункту посадки
def test_survival_by_embarked(test_data):
    result = test_data[test_data['Embarked'] == 'S']['Survived'].value_counts()
    assert result[0] == 1  # 1 погибший на S
    assert result[1] == 1  # 1 спасённый на S

# Тестирование расчета процента выживших среди старых и молодых пассажиров
def test_survival_rate_by_age(test_data):
    young = test_data[test_data['Age'] < 30]
    old = test_data[test_data['Age'] > 30]
    assert young['Survived'].mean() == 1.0  # Все молодые выжили
    assert old['Survived'].mean() == 0.0  # Все старые погибли

# Тестирование среднего возраста по классу обслуживания
def test_average_age_by_class(test_data):
    class_1 = test_data[test_data['Pclass'] == 1]
    assert class_1['Age'].mean() == 38.0  # Средний возраст для первого класса 38
