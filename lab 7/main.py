import xml.etree.ElementTree as ET
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

sns.set(style='whitegrid')

xml_file_path = 'XML.xml'
json_file_path = 'sales_data.json'

tree = ET.parse(xml_file_path)
root = tree.getroot()

items = []
for offer in root.findall(".//offer"):
    name = offer.find("name").text
    price = float(offer.find("price").text)
    items.append({"name": name, "price": price})

with open(json_file_path, 'r', encoding='utf-8') as f:
    sales_json = json.load(f)

data = []
for item in sales_json['sales']:
    row = {'Товар': item['name'], 'Цена, руб.': next(
        (x['price'] for x in items if x['name'] == item['name']), None)}
    for i, sale in enumerate(item['sales'], 1):
        row[f'{i} мес.'] = sale
    data.append(row)

df = pd.DataFrame(data)

predictions = []
true_values = []

for item in sales_json['sales']:
    X = np.arange(1, 13).reshape(-1, 1)
    y = np.array(item['sales'])
    model = LinearRegression().fit(X, y)
    prediction = model.predict([[13]])[0]
    predictions.append(round(prediction, 2))
    true_values.append(y[-1])

df['Прогноз на след. мес.'] = predictions

display(df.style.background_gradient(cmap='Blues'))

rmse = np.sqrt(mean_squared_error(true_values, predictions))
mae = mean_absolute_error(true_values, predictions)

print("\nОценка точности прогноза")
print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")

months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
          "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек", "Следующий"]

fig, axes = plt.subplots(len(items), 1, figsize=(14, 5 * len(items)))
if len(items) == 1:
    axes = [axes]

for ax, item, prediction in zip(axes, sales_json['sales'], predictions):
    sns.lineplot(x=months[:-1], y=item['sales'],
                 marker='o', ax=ax, label='Факт', linewidth=2)
    sns.lineplot(x=months, y=item['sales'] + [prediction], marker='X',
                 linestyle='--', color='orange', ax=ax, label='Прогноз', linewidth=2)
    ax.set_title(f"Динамика продаж: {item['name']}", fontsize=16)
    ax.set_xlabel("Месяц", fontsize=14)
    ax.set_ylabel("Продажи, шт.", fontsize=14)
    ax.legend()

plt.tight_layout()
plt.show()
