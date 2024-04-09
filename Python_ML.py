import serial
import time
import cv2
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


data = pd.read_csv(r"/Users/kavishgajjar/Downloads/Weather_Data (1).csv")
data = data.drop(['Date', 'Temp9am', 'MinTemp', 'MaxTemp', 'Evaporation','WindGustSpeed', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'WindSpeed9am', 'Humidity9am', 'Pressure9am', 'Pressure3pm', 'Cloud9am'] , axis=1)
lb = LabelEncoder()
data['RainToday'] = lb.fit_transform(data['RainToday'])
x = data.iloc[:, [0,3,4,5]].values;
y = data.iloc[:, [1,2]];
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25, random_state = 0)
regression = LinearRegression()
regression.fit(x_train, y_train)


ser = serial.Serial('/dev/tty.usbserial-110', 115200, timeout=1)
time.sleep(2)
while True:
    line = ser.readline().decode("utf-8")
    ldr = int(line[0:2])
    temp = int(line[2:4])
    hum = int(line[4:6])
    wind = int(line[6:8])

    img = cv2.imread(r"/Users/kavishgajjar/Downloads/swiftui-circular-progress-bar-progress-indicator.png")
    y_pred = regression.predict([[temp, ldr, wind, hum]])
    rain_prob = y_pred[0,1]
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 2
    text_color = (56, 40, 39)  # BGR color (Blue, Green, Red)
    thickness = 4
    font2 = cv2.FONT_HERSHEY_DUPLEX
    font_scale2 = 2
    text_color2 = (56, 40, 39)  # BGR color (Blue, Green, Red)
    thickness2 = 3
    text2 = f"Chance of Rain"
    text_size2, _ = cv2.getTextSize(text2, font2, font_scale2, thickness2)
    text_x = (img.shape[1] - text_size2[0]) // 2
    text_y = (img.shape[0] + text_size2[1] - 700) // 2
    cv2.putText(img, text2, (text_x, text_y), font2, font_scale2, text_color2, thickness2)
    variables_dict = {
        'Temperature: ': temp,
        'Sunlight: ': ldr,
        'Wind Speed: ': wind,
        'Humidity: ': hum
    }
    for j, (label, value) in enumerate(variables_dict.items()):
        # Construct text string
        text = f"{label}: {value}"
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_x = (img.shape[1] - text_size[0]) - 20
        text_y = (img.shape[0] - 4*text_size[1] + j*200) // 2
        cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness)
    val = np.interp(float(rain_prob),[0, 1], [-90, 270])
    cv2.ellipse(img, (960, 420), (225, 225), 0, -90, val, (255, 180, 0), 72)
    cv2.imshow("Image", img)
    cv2.waitKey(1)


