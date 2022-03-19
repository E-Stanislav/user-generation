import pandas as pd
import random
from datetime import datetime as DT
from datetime import timedelta
import numpy as np


def data_add_in_company(start, end):
    delta = end - start
    return start + timedelta(random.randint(0, delta.days))


def last_update_in_company(curr_day):
    hours = random.randint(0, 23)
    seconds = random.randint(0, 60)
    minutes = random.randint(0, 60)
    return curr_day + timedelta(hours=hours, minutes=minutes, seconds=seconds)


def get_users():
    start_dt = DT.strptime('01.01.2000', '%d.%m.%Y')
    end_dt = DT.strptime('01.01.2015', '%d.%m.%Y')
    citys = ['Москва', 'Питер', 'Воронеж', 'Суздаль', 'Ярославль']
    curr_day = DT.strptime('19.03.2022 00:00:00', '%d.%m.%Y %H:%M:%S')
    activ_tarif_in_company = [1, 2, 3, 4]
    ids, balans, data_add, year, city, last_update, activ_tarif = [], [], [], [], [], [], []

    count = 1
    for _ in range(50):
        ids.append(count)
        balans.append(random.randint(100, 500))
        data_add.append(data_add_in_company(start_dt, end_dt))
        year.append(random.randint(18, 60))
        city.append(random.choice(citys))
        last_update.append(last_update_in_company(curr_day))
        activ_tarif.append(random.choice(activ_tarif_in_company))
        count += 1

    df = pd.DataFrame([ids, balans, data_add, year, city, last_update, activ_tarif]).transpose()
    df.columns = ['id', 'Текущий баланс', 'Дата добавления', 'Возраст', 'Город проживания',
                  'Временная метка последней активности', 'Активный тариф']
    return df

def get_tarif():
    start_dt = DT.strptime('01.01.2020', '%d.%m.%Y')
    end_dt = DT.strptime('01.01.2022', '%d.%m.%Y')
    names = ['БезПереплат', 'Максимум', 'Супер', 'VIP', 'VipNonStop']

    count = 1
    ids, data_start, data_end, minut, sms, mb = [],[],[],[],[],[]
    for _ in range(5):
        dates = data_add_in_company(start_dt, end_dt)
        ids.append(count)
        data_start.append(dates)
        data_end.append(data_add_in_company(dates, dates + timedelta(random.randint(1000, 4000))))
        minut.append(random.randint(100, 1000))
        sms.append(random.randint(150, 500))
        mb.append(random.randint(1024, 15000))
        count += 1

    tarif = pd.DataFrame([ids, names, data_start, data_end, minut, sms, mb]).transpose()
    tarif.columns = ['id', 'Название','Дата начала действия','Дата конца действия','Объем минут','Объем смс','Объем трафика (мб)']
    return tarif

def activity():
    all_df = pd.DataFrame()
    service = ['звонок', 'смс', 'трафик']
    start_dt = DT.strptime('17.03.2022 00:00:00', '%d.%m.%Y %H:%M:%S')
    end_dt = DT.strptime('19.03.2022 23:59:59', '%d.%m.%Y %H:%M:%S')
    for step in range(1, len(get_users())+1):
        times, id_user, serv, volume = [],[],[],[]
        for _ in range(10):
            times.append(last_update_in_company(data_add_in_company(start_dt, end_dt)))
            id_user.append(step)
            serv.append(random.choice(service))
            volume.append(random.randint(1,10))
        user_df = pd.DataFrame([times, id_user, serv, volume]).transpose()
        all_df = pd.concat([all_df, user_df], axis = 0)
    all_df.columns = ['Метка времени', 'id абонента', 'Тип услуги (звонок, смс, трафик)','Объем затраченных единиц']
    all_df['id'] = np.arange(1, len(all_df)+1)
    all_df = all_df.reindex(columns=['id', 'Метка времени', 'id абонента', 'Тип услуги (звонок, смс, трафик)',
           'Объем затраченных единиц'])
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis = 1, inplace = True)
    return all_df

if __name__ == '__main__':
    get_users().to_csv('src/users.csv', index = False)
    get_tarif().to_csv('src/tarif.csv', index = False)
    user_activity = activity()
    user_activity.to_csv('src/activity.csv', index = False)

    user_activity['day'] = user_activity.apply(lambda x: str(x['Метка времени'])[:10], axis=1)
    table = pd.pivot_table(user_activity, values='Объем затраченных единиц', index=['id абонента', 'day'],
                           columns=['Тип услуги (звонок, смс, трафик)'], aggfunc=np.sum)

    table.columns = [col[1] for col in table.columns]
    table = table.reset_index()
    table.columns = ['Абонент', 'Дата', 'Потрачено минут', 'Потрачено смс', 'Потрачено трафика']
    table = table.fillna(0)
    table.to_csv('src/aggregate_activity.csv', index = False)