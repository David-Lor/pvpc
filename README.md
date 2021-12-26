# pvpc

Repositorio con los precios PVPC, actualizados diariamente mediante Github Actions, utilizando la librería [python-pvpc](https://github.com/David-Lor/python-pvpc).

## Estructura

Los archivos de precios se estructuran de la siguiente forma:

```
data/
├─ cm/ : Datos para Ceuta y Melilla
│  ├─ 2021/ : Año
│  │  ├─ 12/ : Mes
│  │  │  ├─ 26.json : Dia
├─ pcb/ : Datos para Península, Canarias, Baleares
│  ├─ 2021/
│  │  ├─ 12/
│  │  │  ├─ 26.json
```

Cada archivo de día contiene lo siguiente:

```json5
{
  "day": "2021-12-26", // Fecha de los datos, en formato YYYY-MM-DD
  "data": {
    // Claves: horas del día
    // Valores: coste en €/kWh
    "0": 0.29107, // de 0:00h a 1:00h = 0.29107 €/kWh
    "1": 0.25094,
    "2": 0.24032,
    "3": 0.24144,
    "4": 0.19658,
    "5": 0.19161,
    "6": 0.19251,
    "7": 0.22357,
    "8": 0.23473,
    "9": 0.24448,
    "10": 0.25265,
    "11": 0.25593,
    "12": 0.25232,
    "13": 0.24525,
    "14": 0.24518,
    "15": 0.24751,
    "16": 0.2522,
    "17": 0.27027,
    "18": 0.29457,
    "19": 0.30373,
    "20": 0.2916,
    "21": 0.2517,
    "22": 0.23721,
    "23": 0.21941
  }
}
```

## Disclaimer

Los datos de precios, contenidos recursivamente bajo el directorio `data/*`, provienen del portal [PVPC | Esios electricidad](https://www.esios.ree.es/es/pvpc) de Red Eléctrica de España, quien mantiene su autoría.
La reutilización de estos datos se permite bajo ciertas condiciones especificadas en el [Aviso legal - Condiciones respecto al contenido](https://www.esios.ree.es/es/aviso-legal-y-politica-de-privacidad#condiciones-respecto-al-contenido).
