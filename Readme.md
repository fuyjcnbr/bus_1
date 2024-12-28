

## Для генерации файла с моделью (model.pkl) нужно запустить train.py


## Ручная сборка docker образов

```console
dfoo@bar:~$ docker build --squash -t bus_1_features/bus_1_features:latest -f features/Dockerfile features/.

foo@bar:~$ docker build --squash --no-cache -t bus_1_metric/bus_1_metric:latest -f metric/Dockerfile metric/.

foo@bar:~$ docker build --squash --no-cache -t bus_1_model/bus_1_model:latest -f model/Dockerfile model/.

foo@bar:~$ docker build --squash --no-cache -t bus_1_plot/bus_1_plot:latest -f plot/Dockerfile plot/.
```


## Запуск контейнеров
```console
dfoo@bar:~$ docker compose up
```

### Результат работы (absolute_error.png и service_log.csv) появятся в папке service_data
