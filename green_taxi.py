import os
import argparse
import pandas as pd
from time import time
from sqlalchemy import create_engine


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    

    csv_name = 'output.csv.'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)
    # df.lpep_pickup_datetime = pd.to_datetime (df.lpep_pickup_datetime)
    # df.lpep_dropoff_datetime  = pd.to_datetime (df.lpep_dropoff_datetime)

    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True:
        try:
            start = time()
            df = next(df_iter)

            # df.lpep_pickup_datetime = pd.to_datetime (df.lpep_pickup_datetime)
            # df.lpep_dropoff_datetime  = pd.to_datetime (df.lpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')
            end = time()
            print(f'Inserted another chuck.... took {end - start}')
        
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break  


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to postgres")

    parser.add_argument('--user',help='Username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--table_name',help='table name for postgres')
    parser.add_argument('--url',help='url of the csv file')

    args = parser.parse_args()

    main(args)
