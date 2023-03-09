[English: Liga](README.md) | [简体中文：理解机](README_ZH.md)丨[Esperanto: Komprenilo](READEME_EO.md)

# Komprenilo: dancumigu datumojn kun Maŝinlernadaj Modeloj

Komprenilo estas generala kadro por etendi iun ajn SQL-motoron por subteni datumtraktadon uzante Maŝinlernadaj Modeloj. Ĝi havas la sekvajn karakterizaĵojnj:

+ Homamo & Neatako: malfermkoda programaro farita de Terano kaj por homaro
+ Skalebla: facile manipuli datumajn arojn de ajna grandeco
+ Fleksebla kaj facile uzabla: bon-desegnita SQL-etendan sintakson kaj [Python API](README_PYTHON.md)
+ Etendebla: eblas integri kun iu ajn Maŝinlernadaj Modeloj per aldonaĵa mekanismo kaj modelo-registra sistemo

urbazante la kadron de Komprenilo, kun: 
+ Uzant-definita funkcio (UDF)
+ Uzant-definita datumtipo (UDT)
+ Modela Tipo (Model Type)

oni povas provizi domajn-specifajn komprenilajn solvojn


| Domajno | PYPI | Bildiga Ekzemplo | Ekzemplo de Datumtraktado |
|-----|-----------|------------|-|
| Vida Komprenilo | [ligavision](README_VISION.md) | | | |
| Aŭda Komprenilo | | | |
| Naturlingva Komprenilo | | | |
| Prognozilo |  | | | |

## Maŝinlernada Sistemo-Integriĝo
### Kadro por Maŝinlernado
+ [scikit-learn](README_SKLEARN.md)
+ [PyTorch](https://gitee.com/komprenilo/liga-pytorch)

### Model-registra Sistemo
Komprenilo V0.2.x subtenas la model-registran sistemon MLflow, sed tio ne signifas ke Komprenilo nur povas uzi ĉi tiun model-registran sistemon (MLflow).


## Sistema Integriĝo de Datum-Traktado
### Integriĝo kun SQL-motoro
Komprenilo V0.2.x realiĝas surbazante Apache Spark, sed ĝi ne estas alia malfermkoda projekto de Apache Spark. Spark SQL estas nur unu el la SQL-motoroj, al kiuj Komprenilo volas adaptiĝi.

#### SQL: ML_PREDICT
``` sql
SELECT
  id,
  ML_PREDICT(yolov5, image)
FROM cocodataset
```

#### SQL：Krei modelon
``` sql
-- Create model
CREATE [OR REPLACE] MODEL model_name
[USING liga_plugin_name]
[FOR model_type]
[OPTIONS (key1=value1,key2=value2,...)]
```

#### SQL：Administri modelon
``` sql
-- Describe model
{ DESC | DESCRIBE } MODEL model_name;

-- Show all models
SHOW MODELS;

-- Delete a model
DROP MODEL model_name;
```

## Laborfluo 
### Sceno 1: Kompleta laborfluo:
```
Trejnado de modelo -> Konservado en modelo-registrejon -> Kreo de modelo -> Uzado de modelo
```
> Notu: Nuntempe nur subtenas Python por la modelo-trajnado, ne SQL.

### Sceno 2: Se la modelo jam trejniĝis, ĝi povas simpliĝi jene:
```
Kreo de modelo -> Uzado de modelo
```
Estas diversaj modoj por krei modelojn, ekzemple:
+ ŝarĝi publikajn antaŭ-trejnajn modelojn
+ ŝarĝi de privataj modelo-registraj sistemoj
+ ŝarĝi de URL

### Sceno 3: Uzi modelon rekte
```
Uzi modelon
```
> Notu: Ĉi tio dependas de persistanta modelo-katalogo (Model Catalog).

## Historio
Komprenilo devenas de la projekto Rikai. Rikai estas kreita de [Chang She](https://github.com/changhiskhan) kaj [Lei Xu](https://github.com/eddyxu). La unua versio publikiĝis je la 4-an de Aprilo, 2021. En la Kvara Tubi Hackathon, [Darcy Shen](https://github.com/da-tubi) kaj [Renkai Ge](https://github.com/Renkai) kreis la fork-projekton - Komprenilo el Rikai (https://github.com/komprenilo/liga/issues/13).
